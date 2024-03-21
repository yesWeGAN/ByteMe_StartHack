from bs4 import BeautifulSoup
import html

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
    
    # If the text includes encoded characters, use the 'html.unescape()' function
    string = html.unescape(string)
    return string

with open('data.html', 'r', encoding='utf-8') as f:   # encoding added here.
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')


try:
    title = postprocess_strings(soup.find('title').get_text(strip=True))
    title = title.replace(" | sg.ch", "")
except AttributeError:
    title = "Nicht vorhanden"
try:
    description = postprocess_strings(soup.find('meta', attrs={'name': 'description'})['content'])
except AttributeError:
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

address = get_address(soup)

print(f"Title: {title}")
print(f"Beschreibung: {description}")

print(f"Name: {name}")
print(f"Position: {education}")
print(f"Amt: {departement}")
print(f'Address: {address}')
print(f"Telefonnummer: {phone}")
print(f"Email: {email}")
