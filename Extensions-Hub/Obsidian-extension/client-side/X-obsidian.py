from pathlib import Path
from os import write
import requests  
import re
import sys
import os

menu ="""
          
          Usage: X-obsidain.py <option>
          <options>
          
          *query : search for strings in existing notes
          Usage: query <string_to-query>

         *reload : refresh notes in existing obsidian notes location
         Usage: reload 

         *write : write to notes
         Usage: write 

         *export : export .md files to obsadian
         Usage: export <.md/file/locaton>
          """

if len(sys.argv) < 2:
    print(menu, sys.stderr)
    sys.exit(1)

arg1 = sys.argv[1]

def main():
    if arg1 ==  "query":
        if len(sys.argv) != 3:
            print("+ Usage: X-obsidian.py query <string>")
            sys.exit(1)
            arg = sys.argv[2]
        main_query()

    elif arg1 == "reload":
        if len(sys.argv) != 2:
            print("+ Usage: X-obsidian.py reload")
            sys.exit(1)
        reload()

    elif arg1 == "export":
        if len(sys.argv) != 3:
            print("+ Usage: X-obsidian.py export <.md file_location>")
            sys.exit(1)
        export()

    elif arg1 == "write":
        if len(sys.argv) != 2:
            print("+ Usage: X-obsidain.py write")
            sys.exit(1)
        write()

    else:
        print("Option not found")
        print(menu)



def highlight(text, query):
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    highlighted = pattern.sub(f"\033[1;33m{query}\033[0m", text)
    return highlighted


def main_query():
    arg = sys.argv[2]
    url = "http://192.168.81.1:5000/query" #change the ip to the ip of the server exposed to the network
    params = {"q": arg}  

    response = requests.get(url, params=params) 

    if response.status_code == 200:
        data = response.json()
        matches = data.get("matches", [])
        
        for match in matches:
            print(f"\n File: {match['file']}")
            print(f" Snippet:\n{highlight(match['snippet'], arg)}")
            print("-" * 60)
    else:
        print(f" Error: {response.status_code} - {response.text}")


def reload():
    url = "http://192.168.81.1:5000/reload" #change the ip to the ip of the server exposed to the network
    response = requests.get(url)
    print(response.content)
    print(response.status_code)


def export():
    arg = sys.argv[2]
    file_name = arg
    url = "http://192.168.81.1:5000/export" #change the ip to the ip of the server exposed to the network
    with open(file_name, "r", encoding="utf_8") as f:
        files = {"file": (file_name, f)}

        response = requests.post(url, files=files)
        if response.status_code == 200:
            print("File exported successfully.")
        else:
            print(f"Export failed: {response.status_code} - {response.text}")


def write():
    file_name = input("Enter filename: ").strip()
    base_path = Path.cwd()
    write_path = base_path / "tmp"
    write_path.mkdir(parents=True, exist_ok=True)

    full_file_path = write_path / f"{file_name}.md"

    with open(full_file_path, "w", encoding="utf-8") as f:
        content = input("Type your notes here: ")
        f.write(content)

    #Upload it to the server
    url = "http://192.168.81.1:5000/export" #change the ip to the ip of the server exposed to the network
    with open(full_file_path, "rb") as f:
        files = {"file": (full_file_path.name, f)}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            print("File write successful.")
        else:
            print(f"Write failed: {response.status_code} - {response.text}")



if __name__ == "__main__":
    main()

