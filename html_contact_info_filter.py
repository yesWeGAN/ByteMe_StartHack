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
    
    # If the text includes encoded characters, use the 'html.unescape()' function
    string = html.unescape(string)
    return string

with open('data.html', 'r', encoding='utf-8') as f:   # encoding added here.
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

try:
    name = postprocess_strings(soup.find('p', class_='name').get_text(strip=True))
except AttributeError:
    name = "Not found"
try:
    education = postprocess_strings(soup.find('p', class_='education').get_text(strip=True))
except AttributeError:
    education = "Not found"
try:
    departement = postprocess_strings(soup.find('p', class_='departement').get_text(strip=True))
except AttributeError:
    departement = "Not found"
try:
    phone = postprocess_strings(soup.find('a', href=lambda h: h and h.startswith('tel:')).get_text(strip=True))
except AttributeError:
    phone = "Not found"
try:
    email= postprocess_strings(soup.find('a', href=lambda h: h and h.startswith('mailto:')).get_text(strip=True))
except AttributeError:
    email = "Not found"

print(f"Name: {name}")
print(f"Education: {education}")
print(f"Departement: {departement}")
print(f"Phone: {phone}")
print(f"Email: {email}")