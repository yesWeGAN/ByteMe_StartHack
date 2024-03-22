import json

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
with open("/Users/anmyb/Desktop/HACK/contact_dict.json", "r", encoding='utf-8') as f:
    full_dictionary = json.load(f)
paths = ['data/bildung-sport/bslb/Kalender/data', "data/bildung-sport/volksschule/unterricht/fachbereiche/medien-und-informatik/data"]


for path in paths:
    result = search_in_contacts(full_dictionary, path)
    if result is not None:
        print(result)
        break
    else:
        print({'Ansprechpartner':'Empfang', 'Telefonnummer':'+41 58 229 31 11', 'Email':'info@sg.ch'})