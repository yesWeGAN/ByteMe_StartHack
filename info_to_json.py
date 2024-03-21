import os
import json
import re
from bs4 import BeautifulSoup
import html
import string as ring

def postprocess_strings(string):
    string = string.replace("\t", "").replace("\n", "")
    string = string.replace("&auml;", "ä")
    string = string.replace("&ouml;", "ö")
    string = string.replace("&uuml;", "ü")
    string = string.replace("&Auml;", "Ä")
    string = string.replace("&Ouml;", "Ö")
    string = string.replace("&Uuml;", "Ü")
    string = string.replace("&szlig;", "ß")

    string = string.replace("Ã¼", "ü")
    string = string.replace("Ã¤", "ä")
    string = string.replace("Ã¶", "ö")
    string = string.replace("Ãœ", "Ü")
    string = string.replace("Ã„", "Ä")
    string = string.replace("Ã–", "Ö")
    string = string.replace("ÃŸ", "ß")
    string = string.replace("Ã", "Ü")
    string = string.replace("Â", "")
    string = string.replace("«", "")
    string = string.replace("»", "")
    string = string.replace("!", "")
    string = string.replace("â", "")
    string = string.replace("&", "")
    string = string.replace("%", "")
    string = string.replace(",", "")
    string = string.replace(":", "")
    string = string.replace(";", "")
    string = string.replace("(", "")
    string = string.replace(")", "")
    string = string.replace("?", "")
    string = string.replace(".", "")

    
    
    # If the text includes encoded characters, use the 'html.unescape()' function
    string = html.unescape(string)
    return string

# Function to handle German special characters
def convert_umlauts(title):
    umlauts = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue'}
    
    for umlaut, replacement in umlauts.items():
        if umlaut in title:
            title = title.replace(umlaut, replacement)
            
    return title

def filter_string(input_string, valid_chars_list):
    output_string = ''
    for char in input_string:
        if char in valid_chars_list: 
            output_string += char
    return output_string

valid_chars_list = list(ring.ascii_letters) + list(ring.digits) + ['_', '-']
# Function to clean title to be used as a filename
def clean_title(title_text):
    interm = re.sub(r'[^\x00-\x7F]+', '_', title_text)
    return interm.replace(" ", "_").replace("/", "_").replace("-", "_").replace(":", "_")

# Directory to save JSON files
json_dir = 'html_info'

# Parse HTML files
def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')

    # Daten extraktion
    try:
        title = postprocess_strings(soup.find('title').get_text(strip=True))
        title = title.replace("__sgch", "")
    except AttributeError:
        title = "Nicht vorhanden"

    """try:
        description = postprocess_strings(soup.find('meta', attrs={'name': 'description'})['content'])
    except AttributeError:
        description = "Nicht vorhanden"
        """
    description_tag = soup.find('meta', attrs={'name': 'description'}) 
    if description_tag:
        description = postprocess_strings(description_tag['content'])
    else:
        description = "Nicht vorhanden"


    try:
        name = postprocess_strings(soup.find('p', class_='name').get_text(strip=True))
    except AttributeError:
        name = "Nicht vorhanden"
    try:
        education = postprocess_strings(soup.find('p', class_='education').get_text(strip=True))
    except AttributeError:
        education = "Nicht vorhanden"
    try:
        departement = postprocess_strings(soup.find('p', class_='departement').get_text(strip=True))
    except AttributeError:
        departement = "Nicht vorhanden"
    try:
        phone = postprocess_strings(soup.find('a', href=lambda h: h and h.startswith('tel:')).get_text(strip=True))
    except AttributeError:
        phone = "Nicht vorhanden"
    try:
        email= postprocess_strings(soup.find('a', href=lambda h: h and h.startswith('mailto:')).get_text(strip=True))
    except AttributeError:
        email = "Nicht vorhanden"

    def get_address(soup):
        address_tag = soup.find('p', class_='address')
        if not address_tag:
            return "Nicht vorhanden"
        else:
            for br in address_tag.findAll('br'):
                br.replace_with(", ")
            return postprocess_strings(address_tag.get_text())
        
    try:
        address = get_address(soup)
    except AttributeError:
        address = "Nicht vorhanden"

    data = {
        'Titel': title,
        'Beschreibung': description,
        'Name': name,
        'Position': education,
        'Amt': departement,
        'Addresse': address,
        'Telefonnummer': phone,
        'Email': email
    }
    
    elements = file_path.split("/Users/anmyb/Desktop/HACK/data")[-1].split(".html")[0].split("/")
    title="_".join(elements)
    json_file = os.path.join(json_dir, title + '.json')


    try:
        # Write data dictionary to JSON file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except FileNotFoundError as e:
        print(f"Couldn't write json file due to: {e}. Skipping this file.")
        return  # Skip this file and continue with the next one

# Define start directory
start_dir = '/Users/anmyb/Desktop/HACK/data'

# Walk through directory tree, open HTML files
for dir_path, dirs, files in os.walk(start_dir):
    for filename in files:
        if filename.endswith('.html'):
            file_path = os.path.join(dir_path, filename)
            parse_html(file_path)


#aktuelle version