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
endpoint = "api-football-v1.p.rapidapi.com"
headers = {
    'X-RapidAPI-Key': os.getenv("API_TOKEN"),
    'X-RapidAPI-Host': endpoint,
}
league = 4
season = 2024

# Schema specifics
cols = "cols"
name = "name"
type = "type"
api_key = "api_key"
p_key = "primary_key"
f_key = "foreign_key"
f_table = "foreign_table"
schema = {}

with open("schema/schema.json", "r") as file:
    schema = json.loads(file.read())

# SQL generation
def json_flatten(data: list, tokens: list[str], result: list, key=""):
    if isinstance(data, dict):
        if tokens:
            json_flatten(data[tokens[0]], tokens[1:], result, tokens[0])
        else:
            result.append(data)
        return result
    elif isinstance(data, list):
        for item in data:
            json_flatten(item, tokens, result, key)
        return result
    else:
        result.append({key: data})
        return result

def sql_stringify(s: str, t: str):
    if re.match(r"^VARCHAR|^TIMESTAMP", t) != None:
        return "'" + s + "'"
    return s

def sql_generate(query: str, table: str):
    # Fetch data from the API.
    client = http.client.HTTPSConnection(endpoint)
    client.request("GET", query, headers=headers)
    data =  json.loads(client.getresponse().read().decode())

    if not "response" in data:
        print(data)
        return ""

    # The response might have nested properties, so "flatten" it.
    tokens = schema[table][api_key].split(":")
    data = json_flatten(data, tokens, [])
    items = {}

    for item in data:
        for col in schema[table][cols]:
            # skip fields that are not part of the API.
            if col[api_key] == "":
                continue
            tokens = col[api_key].split(":")
            field = json_flatten(item, tokens, [])[0]
            if col[api_key] in items:
                items[col[api_key]].append(field[tokens[-1]])
            else:
                items[col[api_key]] = [field[tokens[-1]]]

    # Create the table, insert the data and append it to the result.
    result = f"CREATE TABLE IF NOT EXISTS {schema[table][name]} (\n"
    p_keys = []
    f_keys = []
    n = len(schema[table][cols])

    for i in range(0, n):
        col = schema[table][cols][i]
        if col[p_key]:
            p_keys.append(col[name])
        if col[f_key]:
            f_keys.append((col[name], col[f_key], col[f_table]))
        if i+1 < n:
            result += f"\t{col[name]} {col[type]},\n"
        else:
            result += f"\t{col[name]} {col[type]}"
    if p_keys:
        result += f",\n\tPRIMARY KEY ({', '.join(p_keys)})"
    if f_keys:
        result += "".join(
            [f",\n\tFOREIGN KEY ({name}) REFERENCES {foreign_table} ({foreign_key})" 
             for (name, foreign_key, foreign_table) in f_keys])
        
    result += "\n);\n\n"
    result += f"INSERT INTO {schema[table][name]} "
    result += f"({', '.join([col[name] for col in schema[table][cols]])}) "
    result += "VALUES \n"
    k = len(data)

    for i in range(0, k):
        for j in range (0, n):
            col = schema[table][cols][j]
            if col[name] == "id":
                if col[api_key] in items:
                    result += f"\t({items[col[api_key]][i]}, "
                else:
                    # Assign naive id.
                    result += f"\t({i}, "
            elif j+1 < n:
                result += f"{sql_stringify(items[col[api_key]][i], col[type])}, "
            elif i+1 < k:
                result += f"{sql_stringify(items[col[api_key]][i], col[type])}),\n"
            else:
                result += f"{sql_stringify(items[col[api_key]][i], col[type])})\n"

    return result + " ON CONFLICT DO NOTHING;\n"

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
    result = ""

    if args["-f"]:
        with open(args["-f"], "r") as file:
            result = file.read()
    else:
        result = sql_generate(f"/v3/teams?league={league}&season={season}", "teams") + "\n"
        result += sql_generate(f"/v3/standings?league={league}&season={season}", "groups") + "\n"
        result += sql_generate(f"/v3/fixtures?league={league}&season={season}", "fixtures")

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