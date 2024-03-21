"""This file takes a folder of JSON-files (parsed from html),
and builds a list of tagged strings that can be indexed and embedded"""

import json
from pathlib import Path

json_dir = "html_info"
json_files = Path(json_dir).rglob("*.json")
index = 0
texts = []
paths = []

for json_file in json_files:

    data = json.load(open(json_file, "r"))
    elements = json_file.as_posix().split("/")[-1].split(".json")[0].split("_")
    elements.remove("data")
    print(f"Elements are: {elements}")

    if len(data["Beschreibung"])<5 or data["Beschreibung"]=="Nicht vorhanden":
        continue

    join_tags = "Bezüglich: "+", ".join(elements)+" "
    tagged_text = join_tags + data["Titel"]+". "+data["Beschreibung"]
    texts.append(tagged_text)
    paths.append(json_file.as_posix().split("html_info/")[-1])
    print(tagged_text)
    print(json_file.as_posix().split("html_info/")[-1])
    #break


    
assert len(texts)==len(paths), "They are not equal!"
len(texts)
