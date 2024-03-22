"""This file takes a folder of JSON-files (parsed from html),
and builds a list of tagged strings that can be indexed and embedded"""

import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import torch
model = SentenceTransformer('intfloat/multilingual-e5-large-instruct')

json_dir = "/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/src/json_files/kb"
json_files = Path(json_dir).rglob("*.json")
index = 0
questions = []
answers = []
embedded_questions = []

for json_file in json_files:
    try:
        data = json.load(open(json_file, "r",encoding='utf-8'))

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
            tagged_question = join_tags+" Frage: " + sub_dict["question"]+" Antwort: "+sub_dict["answer"]

            special_chars = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'}
            for ch, repl in special_chars.items():
                tagged_question = tagged_question.replace(ch, repl)

            questions.append(tagged_question)
            # answers.append(sub_dict["question"])
    except:
        print(json_file.as_posix())
print(questions)
# embed questions
questions_embeddings = model.encode(questions)
# dump original questions
with open(json_dir+"/all_questions.json",'w',encoding='utf-8') as outfile:
  json.dump(questions, outfile)

# dump the embedding stack
q_tensors = [torch.Tensor(embd).unsqueeze(0) for embd in questions_embeddings]
q_tensor_cat = torch.cat(q_tensors)  # is of shape len(questions), embed_dim
saving_path_q = json_dir+"/q_embed_stack.pt"
torch.save(q_tensor_cat,saving_path_q)


    
# assert len(questions)==len(answers), "They are not equal!"
