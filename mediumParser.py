#!/usr/bin/env python3
"""
This application prints the content of users blog and
shows the amount of times a word/phrase appears in the blog
"""
import feedparser
from html.parser import HTMLParser
import requests

globwords = ''
globtag = ''
globCollectTags = []


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global globtag
        global globCollectTags
        if (tag == 'p' or tag == 'li' or tag == 'h4' or tag == 'a' or
                tag == 'h2' or tag == 'h1'):
            globCollectTags.append(tag)
            globtag = tag
        else:
            globtag = ''

    def handle_data(self, data):
        global globwords
        global globtag
        global globCollectTags
        if globtag == 'p':
            if globCollectTags[-2] == 'a':
                globwords += data
            elif globCollectTags[-2] == 'p':
                globwords += '\n\n'
            globwords += data
        # TODO find alternative for considering standard medium data
        elif (globtag == 'a' and 'About membership' not in data and
              'Sign in' not in data and 'Get started' not in data):
            if globCollectTags[-2] == 'p' or globCollectTags[-2] == 'a':
                globwords += data
            elif (globCollectTags[-2] == 'h4' or globCollectTags[-2] == 'h3' or
                  globCollectTags[-2] == 'h2'):
                globwords += '\n' + data
        elif globtag == 'h4' or globtag == 'h2' or globtag == 'h1':
            globwords += '\n\n' + data + '\n\n'
        elif globtag == 'li':
            if globCollectTags[-2] == 'p':
                globwords += '\n'
            globwords += '\n\n\t-' + data


# Access user profile
print('Please enter your username')
username = str(input()).lower()
userProfile = feedparser.parse('https://medium.com/feed/@{}'.format(username))

# Blog to check
print('Please enter a title of your post to check')
blogTitle = str(input())

# Will count the instances of the word in the blog later...
print('Enter the word you want to check for. Please consider punctuation')
userWord = str(input())

# this prints the titles
blogEntry = None
for blog in userProfile.entries:
    if blog.title == blogTitle:
        blogEntry = blog.link

if not blogEntry:
    print('Could not find blog :(')

if blogEntry:
    # Access blog here
    blogPage = requests.get(blogEntry)
    # Init parser
    parser = MyHTMLParser()
    # Remove unicode
    decodedPage = blogPage.content.decode()
    # Time to feed page content! This is where the parsing is initiated!
    parser.feed(str(decodedPage))

    print('Here is your blog content (well sort of for now :)\n\n')
    print(globwords)
    print()
    print('This is the amount of times your search comes up: {}'.format(
        globwords.lower().count(userWord.lower())))
