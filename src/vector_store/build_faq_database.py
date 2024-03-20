import json
from pathlib import Path

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.tag_of_interest =  False

    def handle_starttag(self, tag, attrs):
        if tag == "a":  # tag is the one in brackets: <a>
            for attr in attrs:  # every tag has atttributes. attrs is a list of tuples
                if "collapse" in attr:     # iterate over the tuples and check for keywords
                    print("this one is collapseable and thus a question!")
                    #print(f"Found a a-tag: {tag} with attrs {attrs}")
                    self.tag_of_interest = True    # we only want to print the data if its in a 
        pass

    def handle_endtag(self, tag):   # we do not care about the end tag yet
        # print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):    # this one prints the content of the tag
        if len(data.strip())>0 and self.tag_of_interest:   # most paragraphs contain only whitespace
            # pass
            print("Here's the data of your tag-of-interest:", data)
            self.tag_of_interest = False
    
parser = MyHTMLParser()

# put the path to your FAQ files here
html_faq_files = Path("/Users/FrankTheTank/start/ByteMe_StartHack/src/vector_store").rglob("*.html")
for faq in html_faq_files: 
    print(faq.as_posix())
    with open(faq, 'r') as htmlFile:
        pure_string = htmlFile.read()
        print(pure_string)
        parser.feed(pure_string)