import os
from collections import defaultdict
import json


def build_contact_dict(path_to_json_folder: str):
    contact_dict = defaultdict(list)

    for filename in os.listdir(path_to_json_folder):
        with open(os.path.join(path_to_json_folder, filename)) as json_file:
            real_filename = filename.replace('_', '/')
            contact_dict[real_filename.rstrip('.json')].append(json.load(json_file))

    return contact_dict


test = build_contact_dict("/home/benjaminkroeger/Downloads/html_info")
with open(r'/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/src/qa_search_stack/contact_dict.json', 'w',
          encoding='utf-8') as outfile:
    json.dump(test, outfile, ensure_ascii=False)

print('Hi')
