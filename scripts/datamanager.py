#!/usr/bin/env python3
"""
--------------------------
datamanager
--------------------------
Feel free to change whatever needs changing in this script, 
however make sure that if you call an API endpoint, never do it within a loop,
as my personal credit-card is connected to the API :)
~ Tim Jensen
"""
import sys, os, re, http.client, hashlib, json 
from subprocess import run, DEVNULL
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# Docker specifics
backup_volume = "dis_backups"
backup_dir = "/backups"

# API specifics
endpoints = [
    "api-football-v1.p.rapidapi.com",
    "translated-mymemory---translation-memory.p.rapidapi.com"
    ]
headers = [
    {
        'X-RapidAPI-Key': os.getenv("API_TOKEN"),
        'X-RapidAPI-Host': endpoints[0],
    },
    {
        'X-RapidAPI-Key': os.getenv("API_TOKEN"),
        'X-RapidAPI-Host': endpoints[1],
    }]
league = 4
season = 2024

def fetch(endpoint: str, headers: dict, query: str):
    client = http.client.HTTPSConnection(endpoint)
    client.request("GET", query, headers=headers)
    return json.loads(client.getresponse().read().decode())

# Schema specifics
schema = {}

with open("schema/schema.json", "r") as file:
    schema = json.loads(file.read())

# SQL generation
def json_flatten(data: list[dict|list]):
    result = {}
    for field in data:
        stack = [field]
        while len(stack):
            next = stack.pop()
            if isinstance(next[1], list):
                for item in next[1]:
                    stack.append((next[0], item))
            elif isinstance(next[1], dict):
                for k, v in next[1].items():
                    stack.append((f"{next[0]}:{k}", v))
            else:
                if next[0] in result:
                    result[next[0]].append(next[1]) 
                else:
                    result[next[0]] = [next[1]] 

    return result

def sql_stringify(s: str, t: str):
    if re.match(r"^VARCHAR|^TIMESTAMP", t) != None:
        return "'" + s + "'"
    return s

def sql_from_api(query: str, table: str, localizations: list):
    # Fetch data from the API.
    data =  fetch(endpoints[0], headers[0], query)

    if not "response" in data:
        print(data)
        return ""

    # The response might have nested properties, so "flatten" it.
    data = json_flatten(data.items())

    # Create the table, insert the data and append it to the result.
    cols = schema[table]["cols"]
    p_keys = []
    f_keys = []

    for col in cols:
        if col["primary-key"]:
            p_keys.append(col["name"])
        elif col["foreign-key"]:
            f_keys.append((col["name"], col["foreign-key"], col["foreign-table"]))
        if col["localize"]:
            localizations += [
                (f"{table}:{col['name']}:{data[cols[0]['api-key']][i]}", item)
                for i, item in enumerate(data[col["api-key"]])]

    result = "\n".join([
        f"CREATE TABLE IF NOT EXISTS {schema[table]['name']} (",
        ",\n".join(
            [f"\t{col['name']} {col['type']}" for col in cols] +
            [f"\tPRIMARY KEY ({', '.join(p_keys)})"] +
            [f"\tFOREIGN KEY ({name}) REFERENCES {f_table} ({f_key})" 
                for (name, f_key, f_table) in f_keys]
        ),
        ");\n\n"
        ])
    result += "\n".join([
        "BEGIN TRANSACTION;\n",
        " ".join([
            f"INSERT INTO {schema[table]['name']}",
            f"({', '.join([col['name'] for col in schema[table]['cols']])})",
            "VALUES",
            "\n"
        ])
    ])

    result += "\n".join([
        ",\n".join([
            "\t(" + ", ".join("{0}".format(
            sql_stringify(data[col["api-key"]][i], col["type"])
            if col["api-key"] in data else
            i
            if col["name"] == "id" else
            "")
            for col in cols) + ")"
            for i in range(len(data[col["api-key"]]))
            ]),
        "ON CONFLICT (id) DO UPDATE SET ",
        ",\n".join([f"\t{col['name']} = EXCLUDED.{col['name']}" for col in cols[1:]]),
        ";\n",
    ])

    return result + "COMMIT;"

def sql_from_locales(localizations: list):
    # Get manual localizations.
    locales = []
    cols = schema["locales"]["cols"]
    for col in cols[1:]:
        with open(f"src/locale/{col['name']}.json", "r") as locale:
            locales.append(json.load(locale))

    items = []
    for locale in locales:
        items.append(json_flatten(list(locale.items())[2:]))

    # Create the table, insert the data and append it to the result.
    result = "\n".join([
        "CREATE TABLE IF NOT EXISTS locales (",
        "\tid VARCHAR(255),",
        ",\n".join(
            [f"\t{l['id']} VARCHAR(255)" for l in locales] +
            ["\tPRIMARY KEY (id)"]
            ),
        ");\n\n"
        ])

    result += "\n".join([
        "BEGIN TRANSACTION;\n",
        f"INSERT INTO locales ({', '.join([col['name'] for col in cols])}) VALUES ",
        ",\n".join([
            "\t(" + ", ".join(["'{0}'".format(
            items[i-1][key][0] if i else key) 
            for i in range(len(cols))]) + ")" 
            for key in items[0].keys()
            ]),
        "ON CONFLICT (id) DO UPDATE SET ",
        ",\n".join([f"\t{col['name']} = EXCLUDED.{col['name']}" for col in cols[1:]]),
        ";\n\n"
        ])

    result += "\n".join([
        "INSERT INTO locales (id, en_EN) VALUES ",
        ",\n".join([f"\t('{l[0]}', '{l[1]}')" for l in localizations]),
        "ON CONFLICT (id) DO UPDATE SET en_EN = EXCLUDED.en_EN"
        ";\n\n"
    ])

    # Translate to each locale.
    query = "%3B".join([l[1].replace(" ", "%20") for l in localizations])

    for col in cols[1:]:
        iso = re.match(r"^([a-z]{2})_[A-Z]{2}$", col["name"])[1]
        if not iso or col["name"] == "en_EN":
            continue
        # Fetch data for this locale.
        data =  fetch(endpoints[1], headers[1], f"/get?langpair=en%7C{iso}&q={query}")
        if not "responseData" in data:
            print(data)
            return ""
        items = data["responseData"]["translatedText"].split(";")
        result += "\n".join([
            ";\n".join([
                f"UPDATE locales SET {col['name']} = '{items[i]}' WHERE id = '{l[0]}'" 
                for i, l in enumerate(localizations)
            ]) + ";",
            "\n",
            ]) 

    return result + "COMMIT;"

def backup(args: dict):
    cmd = ["docker", "exec", f"{args['-c']}", "sh", "-c"]
    out = f"{backup_dir}/out"
    dump = run(cmd + [f"pg_dump -U {args['-u']} -d {args['-d']} -Fd -f {out} && ls {out}"], capture_output=True)
    sha = hashlib.sha256()

    for line in dump.stdout.decode().split("\n"):
        if re.match(r".*\.gz$", line) != None:
            content = run(cmd + [f"gunzip -c {out}/{line} | cat"], capture_output=True)
            sha.update(content.stdout)

    name = f"{backup_dir}/{sha.hexdigest()}"
    rm = run(cmd + [f"rm -rf {name}"])
    mv = run(cmd + [f"mv -uf -T {out} {name}"])

    if dump.returncode or rm.returncode or mv.returncode:
        print(f"exiting: failed to backup \"{args['-d']}\".")
        return 1
    
    print(f"backed up \"{args['-d']}\" as \"{name}\".")
    return 0

def populate(args: dict):
    # Backup the database before proceding.
    if backup(args):
        return 1

    # Generate data and write to db.
    localizations = []
    result = ""

    if args["-f"]:
        with open(args["-f"], "r") as file:
            result = file.read()
    else:
        result = sql_from_api(f"/v3/teams?league={league}&season={season}", "teams", localizations) + "\n"
        result += sql_from_api(f"/v3/standings?league={league}&season={season}", "groups", localizations) + "\n"
        result += sql_from_api(f"/v3/fixtures?league={league}&season={season}", "fixtures", localizations) + "\n"
        result += sql_from_locales(localizations)

    p = run(["docker", "exec", f"{args['-c']}", "sh", "-c", f'echo "{result}" | psql -U {args["-u"]} -d {args["-d"]}'], stdout=DEVNULL, stderr=DEVNULL)

    if p.returncode:
        print(f"exiting: failed to populate \"{args['-d']}\".")
        return 1

    print(f"populated \"{args['-d']}\" successfully.")
    return 0

def dump(args: dict):
    # Dump the database.
    path = os.path.abspath(args["-o"])
    dir = os.path.dirname(path)
    file = os.path.basename(path)
    p = run(["docker", "exec", f"{args['-c']}", "sh", "-c", f"pg_dump -U {args['-u']} -d {args['-d']} | cat"], capture_output=True)

    if p.returncode:
        print(f"exiting: failed to dump \"{file}\".")
        return 1
    
    if not os.path.isdir(dir):
        os.makedirs(dir)

    with open(path, "w") as out:
        out.write(p.stdout.decode())

    print(f"dumped \"{os.path.join(dir, file)}\" successfully.")
    return 0

def restore(args: dict):
    cmd =  ["docker", "exec", f"{args['-c']}"]
    dir = f"{backup_dir}/{args['-f']}"

    if "-ls" in args:
        cmd = cmd + ["sh", "-c"]

        if args["-f"]:
            dump = run(cmd + [f"ls {dir}"], capture_output=True)

            for line in dump.stdout.decode().split("\n"):
                if re.match(r".*\.gz$", line) != None:
                    content = run(cmd + [f"gunzip -c {dir}/{line} | cat"], capture_output=True)
                    print(content.stdout.decode())
        else:
            run(cmd + [f"ls -g --time creation {backup_dir}/"])
        return 0
    elif args["-f"]:
        if backup(args):
            return 1
        
        # No mercy restore
        p = run(cmd + ["pg_restore", "-U", f"{args['-u']}", "-d", f"{args['-c']}", "-c", "-C", f"{backup_dir}/{args['-f']}"])

        if p.returncode:
            print(f"exiting: failed to restore \"{args['-d']}\".")
            return 1
        else:
            print(f"restored \"{args['-d']}\" successfully.")
        return 0
    return 1

if __name__ == "__main__":
    command = ""
    args = {
        "-c": os.getenv("DB"), 
        "-d": os.getenv("POSTGRES_DB"), 
        "-u": os.getenv("POSTGRES_USER"),
        "-o": "schema/schema.sql",
        "-f": ""
        }

    if len(sys.argv) > 1:
        command = sys.argv[1]
    if len(sys.argv) > 2:
        for i in range(2, len(sys.argv)):
            if re.match(r"^-([cdfou])$", sys.argv[i]) != None:
                args[sys.argv[i]] = sys.argv[i+1]
            elif re.match(r"^-ls$", sys.argv[i]):
                args[sys.argv[i]] = True


    # Make sure that a container is running.
    p = run(["docker", "container", "inspect", "-f", ".State.Running", f"{args['-c']}"], stdout=DEVNULL)

    if p.returncode:
        print(f"exiting: container \"{args['-c']}\" must be running.")
        exit(1)

    if command == "populate" and not populate(args):
        exit(0)
    elif command == "dump" and not dump(args):
        exit(0)
    elif command == "restore" and not restore(args):
        exit(0)

    print(f"""datamanager.py command [options]

Usage:
    populate\t[-f <file>] [-c <string>] [-d <string>] [-u <string>]
    dump\t[-c <string>] [-d <string>] [-u <string>] [-o <path>]
    restore\t(-ls [-f <file>] | -f <file>]) [-c <string>] [-d <string>] [-u <string>]

Options:
    -c\t\tName of the docker container. Defaults to "{args['-c']}"
    -d\t\tName of the PostgreSQL database. Defaults to "{args['-d']}"
    -u\t\tName of the PostgreSQL user. Defaults to "{args['-u']}"
    -o\t\tOutput path. Defaults to "schema/schema.sql"
    -ls\t\tLists all or a specific backup.
    -f\t\tSpecifies a file to use.
    -h, --help\tShows this message.""")
    exit(0)
