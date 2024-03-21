import json
from pathlib import Path
import os
import html

from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.tag_of_interest =  False
        self.is_question = False
        self.is_answer = False
        self.prev_was_question = False
        self.prev_was_answer = False
        self.prev_question_answered = False
        self.buffer_question = None
        self.q_and_a = {}

    def handle_starttag(self, tag, attrs):
        if tag == "a":  # tag is the one in brackets: <a>
            for attr in attrs:  # every tag has atttributes. attrs is a list of tuples
                if "collapse" in attr:     # iterate over the tuples and check for keywords
                    # print("this one is collapseable and thus a question!")
                    #print(f"Found a a-tag: {tag} with attrs {attrs}")
                    self.tag_of_interest = True    # we only want to print the data if its in a 
                    self.is_question = True
        if tag == "div":
            for attr in attrs: 
                if "col-xs-12" in attr:
                    self.tag_of_interest = True
                    self.is_answer = True

    def handle_endtag(self, tag):   # we do not care about the end tag yet
        # print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):    # this one prints the content of the tag
        if len(data.strip())>0 and self.tag_of_interest:   # most paragraphs contain only whitespace
            # pass
            # print(data)
            if self.is_question:
                
                if self.prev_was_question:
                    print(f"Previous question was not answered!{data}")
                else:
                    self.buffer_question = data
                    self.prev_was_question = True
                self.prev_was_answer = False

            if self.is_answer:
                
                if self.prev_was_answer:
                    print(f"Answer without a question: {data}")
                else:
                    self.q_and_a[self.buffer_question]=data
                    self.prev_was_answer = True
                self.prev_was_question = False

            self.tag_of_interest = False
            self.is_answer = False
            self.is_question = False

    
parser = MyHTMLParser()

# put the path to your FAQ files here
html_faq_files = Path("/Users/FrankTheTank/Downloads/data").rglob("**/*faq*")
for path in html_faq_files:
    faq = next(iter(Path(path).rglob("*.html")))
    with open(faq, 'r', encoding='iso-8859-15') as htmlFile:
        pure_string = htmlFile.read()
        # print(pure_string)
        parser.set_filepath = faq.as_posix()
        parser.feed(pure_string)

parser.q_and_a
filtered_q_and_a = {}


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

for q, a in parser.q_and_a.items():
    if q and "?" in q:
        print("Question: ")
        print(q)
        print("Answer:")
        print(a)
        filtered_q_and_a[postprocess_strings(q)]=postprocess_strings(a)

with open("q_and_a.json", 'w', encoding='utf-8') as jsonout:
    json.dump(filtered_q_and_a, jsonout)
len(filtered_q_and_a)

import json
fuqs = json.load(open("src/vector_store/1.json", 'r'))
fuqs
from pprint import pprint
pprint(fuqs)