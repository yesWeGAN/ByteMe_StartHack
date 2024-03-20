from bs4 import BeautifulSoup

def html_to_text(html_file):
    with open(html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        text = soup.get_text()
    return text

# Usage example
html_file = 'C:/Users/anmyb/Desktop/HACK/data/data/bildung-sport/berufsbildung/itbo-berufsbildung/data.html'
text = html_to_text(html_file)
print(text)

