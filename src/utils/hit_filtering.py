import json

with open("/home/benjaminkroeger/Documents/Hackathons/StartHack24/ByteMe_StartHack/src/qa_search_stack/contact_dict.json", "r",
          encoding='utf-8') as f:
    full_dictionary = json.load(f)


def filter_hits_threshold(questions: list[str], answers: list[str]) -> tuple[list[str], list[str]]:
    filtered = [(q, a) for q, a in zip(questions, answers)]
    return zip(*filtered)


def create_summary_str(questions: list[str], answers: list[str], original_question: str):
    summary_str = ['\n\n']
    for question, answer in zip(questions, answers):
        summary_str.append(f'{question}: {answer}\n')
    summary_str = ''.join(summary_str)
    summary_str = original_question + summary_str

    return summary_str


def restructure_contact_urls(faiss_seperator: str, contact_dict_seperator, filenames: list[str]) -> list[str]:
    renamed_names = []

    for filename in filenames:
        new_name = filename.replace(faiss_seperator, contact_dict_seperator).rstrip('.json')
        renamed_names.append(new_name)

    return renamed_names


def search_json(full_dictionary, path):
    try:
        return full_dictionary[path]
    except KeyError:
        return None


def search_in_contacts(full_dictionary, path):
    print(path)

    contact_list = search_json(full_dictionary, path)

    contact = contact_list[0]
    if contact['Name'] != "Nicht vorhanden":
        result = {}
        result["Name"] = contact['Name']
        result["Telefonnummer"] = contact['Telefonnummer']
        if contact['Email'] != "Nicht vorhanden":
            result["Email"] = contact['Email']
            return result
        return result
    if contact['Amt'] != "Nicht vorhanden":
        result = {}
        result["Amt"] = contact['Amt']
        result["Telefonnummer"] = contact['Telefonnummer']
        if contact['Email'] != "Nicht vorhanden":
            result["Email"] = contact['Email']
            return result
        return result


# Load data from JSON file

def get_best_contact(paths:list[str]):
    for path in paths:
        result = search_in_contacts(full_dictionary, path)
        if result is not None:
            return result
        else:
            return {'Ansprechpartner': 'Empfang', 'Telefonnummer': '+41 58 229 31 11', 'Email': 'info@sg.ch'}
