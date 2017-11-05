#!/usr/bin/env python3
import feedparser
from html.parser import HTMLParser
import requests

#print("Please enter your username lowercase")
#userInput = str(input())
#userInput = 'joewmcdaniel'
userInput = 'joewmcdaniel'

#print("Please enter a title of your post to check")
#userTitle = str(input())
#userTitle = 'Find all files of a certain type in the local directory!'
#userTitle = 'What happens when you type ls -l in the shell'
userTitle = 'The timeless web stack question'

#print("Enter the word you want to check for")
#userWord = str(input())

#user = feedparser.parse('https://medium.com/feed/@joewmcdaniel')
user = feedparser.parse('https://medium.com/feed/@{}'.format(userInput))

#entry= ''
# this prints the titles
for title in user.entries:
    # print title.title
    if title.title == userTitle:
        entry = title.link
        #print(entry)


# this gets the code from the page
page = requests.get(entry)

#print("This is the page: {}".format(page))

#page = requests.get('https://medium.com/@spacexengineer/the-journey-to-a-website-9d31635feb99?source=rss-671748f9254------2')

globwords = ''
globtag = ''

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        #return tag
        #def handle_endtag(self, tag):
        #   print("Encountered an end tag :", tag)

        global globtag
        if tag == 'p' or tag == 'h4' or tag == 'a' or tag == 'h2' or tag == 'h1':
            globtag = tag
        #    print('p tag found')
        else:
            globtag = ''
    def handle_data(self, data):
        #print("data handeled")
        global globwords
        global globtag
        if globtag == 'p':
            globwords += "\n" + data + '\n'
        elif globtag == 'a':
            globwords += data
        elif globtag == 'h4' or globtag == 'h2' or globtag == 'h1':
            globwords += data + "\n"
        #print("Encountered some data  :", data)


#parser = MyHTMLParser()
#parser.feed(str(page.content))


parser = MyHTMLParser()
parser.feed(str(page.content))
print("This is the value for globwords: \n\n\n\n{}".format(globwords))

#print("\n\n\n\n")


#filteredWords = ''.join(e for e in globwords if e.isalnum())
#print(filteredWords)
print("\n\n\n\n\n")
print(globwords.count("Web server"))


"""
\xc2\xa0 = nonbreaking space
add later x.replace("\xc2\xa0", " ")

\xe2\x80\xa6 = ...
x.replace("\xe2\x80\xa6", "...")
"""
