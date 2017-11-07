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
globhead = ''
globsection = ''
one_section = 0
glob_list_item = ''


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global globtag
        global globsection
        global globhead
        global glob_list_item

        # finds title tag to print title
        if tag == 'title':
            globtag = 'start title'

        # all desired text in the first section tag
        if tag == 'section' and globsection != 'start section':
            globsection = 'start section'

        # check for headers to print since these are not in the paragraph tags
        if (globsection == 'start section' and
                tag in ['h2', 'h3', 'h4'] and globhead == ''):
            globhead = 'start head'

        # check for list tags since they are outside paragraph tags
        if tag == 'li' and one_section == 0:
            glob_list_item = 'li'

        # all the rest of the text can be found in the paragraph tags!
        if tag == 'p' and (globtag == 'end p' or globtag == ''):
            globtag = 'start ' + tag

    def handle_endtag(self, tag):
        global globtag
        global globwords
        global section
        global one_section

        # This checks if the first section tag is done
        # stops gathering data if true
        if tag == 'section':
            globsection = 'end section'
            one_section = 1

        # Add new lines inbetween paragraphs
        if tag == 'p' and globtag == 'start p':
            globtag = 'end ' + tag
            globwords += '\n\n'

    def handle_data(self, data):
        global globtag
        global globwords
        global globhead
        global globsection
        global one_section
        global glob_list_item

        # add the title data once here
        if globtag == 'start title':
            globwords += data + '\n\n'
            globtag = ''

        # add header data
        if (globhead == 'start head' and globsection != 'end section' and
                one_section == 0):
            globwords += data + '\n\n'
            globhead = ''

        # add list item data
        if glob_list_item == 'li' and one_section == 0:
            globwords += '\t- ' + data + '\n\n'
            glob_list_item = ''

        # add all the rest of the text data in the first section
        if (globtag == 'start p' and globsection == 'start section' and
                one_section == 0):
            globwords += data

# Access user profile
print('Please enter your username')
username = str(input()).lower()
userProfile = feedparser.parse('https://medium.com/feed/@{}'.format(username))

# Blog to check
print('Please enter a title of your post to check')
blogTitle = str(input())
blogTitle = ''.join(e for e in blogTitle if e.isalnum())

# Will count the instances of the word in the blog later...
print('Enter the word you want to check for. Please consider punctuation')
userWord = str(input())

# this prints the titles
blogEntry = None
for blog in userProfile.entries:
    # remove special characters, NOTE possible issue
    if ''.join(e for e in blog.title if e.isalnum()) == blogTitle:
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
