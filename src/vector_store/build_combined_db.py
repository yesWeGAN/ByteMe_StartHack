"""This file takes a folder of JSON-files (parsed from html),
and builds a list of tagged strings that can be indexed and embedded"""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import torch
import os

model = SentenceTransformer('intfloat/multilingual-e5-large-instruct')

json_dir = "html_info"
qa_dir = "/Users/FrankTheTank/start/ByteMe_StartHack/src/json_files/adjusted_qa"
output_directory = "/Users/FrankTheTank/start/ByteMe_StartHack/src/dummy"

os.makedirs(output_directory, exist_ok=True)
json_files = Path(json_dir).rglob("*.json")
qa_files = Path(qa_dir).rglob("*.json")

texts = []
paths = []

for json_file in json_files:

    data = json.load(open(json_file, "r", encoding='utf-8'))
    elements = json_file.as_posix().split("/")[-1].split(".json")[0].split("_")
    elements.remove("data")
    # print(f"Elements are: {elements}")

    if len(data["Beschreibung"]) < 5 or data["Beschreibung"] == "Nicht vorhanden":
        continue

    join_tags = "Bezueglich: " + ", ".join(elements) + " "
    tagged_text = join_tags + data["Titel"] + ". " + data["Beschreibung"]
    special_chars = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue','Ã¼':'ue','Ã¤':'ae','Ã¶':'oe'}
    for ch, repl in special_chars.items():
        tagged_text = tagged_text.replace(ch, repl)

    texts.append(tagged_text)
    paths.append(json_file.as_posix().split("html_info/")[-1])
    print(tagged_text)


assert len(texts) == len(paths), "They are not equal before QA!"

# here come the adjusted QA entries
for json_file in qa_files:

    data = json.load(open(json_file, "r",encoding='utf-8'))
    elements = json_file.as_posix().split("/")[-1].split(".json")[0].split("_")
    elements.remove("data")
    print(f"Elements are: {elements}")
    for sub_dict in data:
        if "tags" in sub_dict.keys():
            join_tags = "Bezueglich: "+", ".join(elements)+" "+", ".join(sub_dict["tags"])+": "
        else:
            join_tags = "Bezueglich: "+", ".join(elements)+" "
        tagged_question = join_tags+" Frage: " + sub_dict["question"]+" Antwort: "+sub_dict["answer"]

        special_chars = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'}
        for ch, repl in special_chars.items():
            tagged_question = tagged_question.replace(ch, repl)

        texts.append(tagged_question)
        paths.append(json_file.as_posix().split("adjusted_qa/")[-1])
    
assert len(texts) == len(paths), "They are not equal after QA!"

questions_embeddings = model.encode(texts)

# dump original texts and paths
with open(os.path.join(output_directory, "all_questions.json"), 'w', encoding='utf-8') as outfile:
    json.dump(texts, outfile)
with open(os.path.join(output_directory, "all_paths.json"), 'w', encoding='utf-8') as outfile:
    json.dump(paths, outfile)

# dump the embedding stack
q_tensors = [torch.Tensor(embd).unsqueeze(0) for embd in questions_embeddings]
q_tensor_cat = torch.cat(q_tensors)  # is of shape len(questions), embed_dim
saving_path_q = output_directory + "q_embed_stack.pt"
torch.save(q_tensor_cat, saving_path_q)
