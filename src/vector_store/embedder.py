import json
from pathlib import Path

json_dir = "/Users/FrankTheTank/start/ByteMe_StartHack/src/json_files/kb"
json_files = Path(json_dir).rglob("*.json")
index = 0
questions = []
answers = []
embedded_questions = []
for json_file in json_files:
    try:
        data = json.load(open(json_file, "r"))
        assert isinstance(data[0], str), "First element is not a string!"
        elements = data[0].split(".ch/")[-1].split(".html")[0].split("/")
        print(f"Elements are: {elements}")
        for sub_dict in data:
            if isinstance(sub_dict, str):
                continue
            if "tags" in sub_dict.keys():
                join_tags = "Bezüglich: "+", ".join(elements)+" "+", ".join(sub_dict["tags"])+": "
            else:
                join_tags = "Bezüglich: "+", ".join(elements)+" "
            tagged_question = join_tags + sub_dict["question"]
            questions.append(tagged_question)
            answers.append(sub_dict["question"])
    except:
        print(json_file.as_posix())

    
assert len(questions)==len(answers), "They are not equal!"
