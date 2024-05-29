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
backup_dir = "/backups"

# API specifics
endpoints = [
    "api-football-v1.p.rapidapi.com",
    "google-translate113.p.rapidapi.com"
    ]
headers = [
    {
        'X-RapidAPI-Key': os.getenv("API_TOKEN"),
        'X-RapidAPI-Host': endpoints[0],
    },
    {
        'X-RapidAPI-Key': os.getenv("API_TOKEN"),
        'X-RapidAPI-Host': endpoints[1],
        'Content-Type': "application/json"
    }]
league = 4
season = 2024

def fetch(method: str, endpoint: str, headers: dict[str, str], query: str = "", body: str = "" ):
    client = http.client.HTTPSConnection(endpoint)
    client.request(method, query, body, headers)
    return json.loads(client.getresponse().read().decode())

# Schema specifics
schema = {}

with open("schema/schema.json", "r") as file:
    schema = json.loads(file.read())

# SQL generation
def json_flatten(data: list[dict|list], key="", result: dict[str, list]={}):
    if isinstance(data, list):
        for item in data:
            json_flatten(item, key, result)
    elif isinstance(data, dict):
        for k in data:
            json_flatten(data[k], key + k + ":", result)
    else:
        key = key.rstrip(":")
        if key in result:
            result[key].append(data)
        else:
            result[key] = [data] 

    return result


def sql_stringify(s: str|int, t: str) -> str:
    if s != "NULL" and re.match(r"^VARCHAR|^TIMESTAMP", t) != None:
        return "'" + s + "'"
    return str(s)

def sql_from_api(query: str, table: str, data: dict[str, list]):
    # Fetch data from the API.
    resp = fetch("GET", endpoints[0],  headers[0], query)

    if not "response" in resp:
        print(resp)
        return ""

    # The response might have nested properties, so "flatten" it.
    tokens = schema[table]["api-key"].split(":")
    while len(tokens):
        if isinstance(resp, list):
            resp = resp[0]
            continue
        resp = resp[tokens.pop(0)]
    if schema[table]["limit"]:
        resp = resp[:schema[table]["limit"]]
    resp = json_flatten(resp, table + ":", {})
    data.update({**resp, **data})

    # Create the table, insert the data and append it to the result.
    cols, rows, p_keys, f_keys = schema[table]["cols"], {}, [], []

    for col in cols:
        if col["api-key"] in resp:
            if col["dedupe"]:
                rows[col["name"]] = list(dict.fromkeys(resp[col["api-key"]]))
            else:
                rows[col["name"]] = resp[col["api-key"]]
            if not "id" in rows:
                rows["id"] = [i for i in range(len(rows[col["name"]]))]
        if col["primary-key"]:
            p_keys.append(col["name"])
        if col["foreign-key"]:
            f_keys.append((col["name"], col["foreign-table"], col["foreign-key"]))
        if col["localize"]:
            for i, item in enumerate(rows[col["name"]]):
                data["localizations"].append(("{0}:{1}:{2}".format(table, col["name"], rows["id"][i]), item))

    result = "BEGIN;\n\n"
    result += "CREATE TABLE IF NOT EXISTS {0} (\n{1}\n);\n\n".format(
        schema[table]["name"],
        ",\n".join(
            ["\t{name} {type}".format(**col) for col in cols] +
            ["\tPRIMARY KEY ({0})".format(", ".join(p_keys))] +
            ["\tFOREIGN KEY ({0}) REFERENCES {1} ({2}) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED".format(*f_key) for f_key in f_keys]
        )   
    )
    result += "INSERT INTO {0} ({1}) VALUES\n{2}\nON CONFLICT (id) DO UPDATE SET\n{3}\n;\n\n".format(
        schema[table]["name"], 
        ", ".join([col["name"] for col in cols if col["name"] in rows]),
        ",\n".join([
            "\t({0})".format(", ".join([
                sql_stringify(rows[col["name"]][i], col["type"]) for col in cols if col["name"] in rows
            ]))
            for i in range(len(rows["id"]))            
        ]),
        ",\n".join(["\t{0} = EXCLUDED.{0}".format(col["name"]) for col in cols[1:] if col["name"] in rows]),
    )

    for col in cols:
        if col["name"] in rows:
            continue
        row = data["rows"][col["foreign-table"]][col["foreign-key"]]
        result += "{0}\n\n".format(
            "\n".join([
                "UPDATE {0} SET {1} = {2} WHERE (id) = {3};".format(
                    schema[table]["name"], 
                    col["name"],
                    row[i//(len(data[col["api-key"]])//len(row))],
                    lid
                ) 
                for lid in rows["id"] 
                for i, fid in enumerate(data[col["api-key"]]) if fid == lid
            ])
        )

    data["rows"][table] = rows

    return result + "COMMIT;\n\n"

def sql_from_locales(data: dict[str, tuple[str]],):
    # Get manual localizations.
    cols, locales = schema["locales"]["cols"], []

    items = []
    for file in os.listdir("./src/locale"):
        with open (f"./src/locale/{file}", "r") as locale:
            locales.append(json.load(locale))

    query, queries = ";".join([s[1] for s in data["localizations"]]), []
    if len(query) > 500: # Hard limit from API
        i = query[0:500].rfind(";")
        queries.append(query[:i])
        query = query[i+1:]
    queries.append(query)

    for locale in locales:
        iso = re.match(r"^([a-z]{2})_[A-Z]{2,3}$", locale["id"])
        if not iso:
            continue
        # Fetch data for this locale.
        items = []
        for query in queries:
            if iso[1] == "en":
                items += query.split(";")
                continue
            resp = fetch("POST", endpoints[1],  headers[1], "/api/v1/translator/text", json.dumps({"from": "en", "to": iso[1], "text": query}))
            if not "trans" in resp:
                print(resp)
                return ""
            items += resp["trans"].split(";")
        for i, s in enumerate(data["localizations"]):
            tokens = s[0].split(":")
            l = locale
            while len(tokens) > 1:
                l = l.setdefault(tokens.pop(0), {})
            l[tokens[0]] = items[i]

    result = "BEGIN;\n\n"
    result += "CREATE TABLE IF NOT EXISTS {0} (\n{1}\n);\n\n".format(
        schema["locales"]["name"],
        ",\n".join(
            ["\t{name} {type}".format(**col) for col in cols] +
            ["\tPRIMARY KEY (id)"]       
        ),
    )

    result += "INSERT INTO {0} ({1}) VALUES\n{2} ON CONFLICT (id) DO UPDATE SET\n{3};\n\n".format(
        schema["locales"]["name"],
        ", ".join([col["name"] for col in cols]),
        ",\n".join([
            "\t({0})".format(",".join([
                "'{0}'".format(locale["id"] if col["name"] == "id" else json.dumps(locale))
                 for col in cols
                ]))
            for locale in locales
        ]),
        ",\n".join(["\t{0} = EXCLUDED.{0}".format(col["name"]) for col in cols[1:]]),
    )

    return result + "COMMIT;\n\n"

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
    if args["-f"]:
        with open(args["-f"], "r") as file:
            result = file.read()
    else:
        data = {"rows": {}, "localizations": []}
        result = sql_from_api(f"/v3/standings?league={league}&season={season}", "groups", data) 
        result += sql_from_api(f"/v3/teams?league={league}&season={season}", "teams", data) 
        result += sql_from_api(f"/v3/fixtures?league={league}&season={season}", "fixtures", data) 
        result += sql_from_locales(data)

    p = run(["docker", "exec", "-i", args["-c"], "psql", "-U", args["-u"], "-d", args["-d"]], input=result, text=True)
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
    p = run(["docker", "exec", f"{args['-c']}", "sh", "-c", f"pg_dump -U {args['-u']} -t \'{args['-t']}\' -c --if-exists {args['-d']} | cat"], capture_output=True)
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
        "-t": "*",
        "-f": "",
        "-t": "public.*",
        "-f": "",
    }

    if len(sys.argv) > 1:
        command = sys.argv[1]
    if len(sys.argv) > 2:
        for i in range(2, len(sys.argv)):
            if re.match(r"^-([cduotf])$", sys.argv[i]) != None:
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
    -t\t\tName of a table. Defaults to all.
    -t\t\tName of a table. Defaults to all.
    -o\t\tOutput path. Defaults to "schema/schema.sql"
    -ls\t\tLists all or a specific backup.
    -f\t\tSpecifies a file to use.
    -h, --help\tShows this message.""")
    exit(0)
