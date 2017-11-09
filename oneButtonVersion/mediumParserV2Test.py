#!/usr/bin/env python3
"""
This application prints the content of users blog and
shows the amount of times a word/phrase appears in the blog
"""
from cpython.Lib.html.parser import HTMLParser
import feedparser
import requests


returned_content = ''


class MyHTMLParser(HTMLParser):
    """
    Parse the information from the provided link
    """

    def handle_starttag(self, tag, attrs):
        """
        Locates all start tags
        """
        # finds title tag to print title
        if tag == 'title':
            self.target_tag = 'start title'

        # all desired text in the first section tag
        if tag == 'section' and self.target_section != 'start section':
            self.target_section = 'start section'

        # check for headers to print since these are not in the paragraph tags
        if (self.target_section == 'start section' and
                tag in ['h2', 'h3', 'h4'] and self.target_head == ''):
            self.target_head = 'start head'

        # check for list tags since they are outside paragraph tags
        if tag == 'li' and self.one_section == 0:
            self.list_item = 'li'

        # all the rest of the text can be found in the paragraph tags!
        if tag == 'p' and (self.target_tag == 'end p' or self.target_tag == ''):
            self.target_tag = 'start ' + tag

    def handle_endtag(self, tag):
        """
        Locates all end tags
        """
        # Checks if the first section tag is done NOTE BUG for other sections
        # stops gathering data if true
        if tag == 'section' and self.one_section != 1:
            self.target_section = 'end section'
            self.one_section = 1
            self.get_content()

        # Add new lines inbetween paragraphs
        if tag == 'p' and self.target_tag == 'start p':
            self.target_tag = 'end ' + tag
            self.content += '\n\n'

    def handle_data(self, data):
        """
        returns data found between tags
        """
        # add the title data once here
        if self.target_tag == 'start title':
            self.content += data + '\n\n'
            self.target_tag = ''

        # add header data
        if (self.target_head == 'start head' and self.target_section != 'end section' and
                self.one_section == 0):
            self.content += data + '\n\n'
            self.target_head = ''

        # add list item data
        if self.list_item == 'li' and self.one_section == 0:
            self.content += '\t- ' + data + '\n\n'
            self.list_item = ''

        # add all the rest of the text data in the first section
        if (self.target_tag == 'start p' and self.target_section == 'start section' and
                self.one_section == 0):
            self.content += data

    def get_content(self):
        """
        Collect all text in content
        """
        global returned_content
        returned_content += self.content
        self.content = ''


def access_profile(username):
    """
    Access RSS feed from a provided username
    """
    user_profile_feed = feedparser.parse(
        'https://medium.com/feed/@{}'.format(username))
    return user_profile_feed


def generate_titles(user_profile_feed):
    """
    Generates a list of titles from the profile entered
    """
    if user_profile_feed:
        titles = {}
        for entry in user_profile_feed.entries:
            titles[entry.title] = entry.link
        return titles


def choose_title(chosen_titles, titles):
    """
    generate dictionary of chosen titles
    """
    chosen = {}
    for title in chosen_titles:
        if title in titles:
            chosen[title] = titles[title]
    return chosen


def generate_content(titles, words):
    """
    generates content from selected titles
    """
    global returned_content
    content = []
    if titles:
        # Init parser
        for title, link in titles.items():
            # Access blog here
            blogPage = requests.get(link)

            # Remove unicode
            decodedPage = blogPage.content.decode()

            # Time to feed page content! This is where parsing is initiated!
            MyHTMLParser().feed(str(decodedPage))

            content.append(returned_content)
            returned_content = ''

        content = ' '.join(content)
        finds = count_words(content, words)
        return_content = ''
        return finds


def count_words(content, words):
    """
    count the number of occurances a word, words, or phrase happens in a blog
    """
    finds = {}
    if content:
        for phrase in words:
            finds[phrase] = content.lower().count(phrase.lower())
            print('This is the amount of times {} comes up: {}'.format(
                phrase, content.lower().count(phrase.lower())))
        return finds


"""
Testing in console

print("Start Test")

feed = access_profile('spacexengineer')
print("profile accessed")

titles = generate_titles(feed)
print('feed completed')

chosen = choose_title(['The Journey To A Website', 'Creating a Dynamic (Shared ) Library In C'], titles)
#print(chosen)
#print(titles)
print("here is the chosen title info: ", chosen)

print("start generating content")
something = generate_content(chosen, ['web server', 'linux'])
print("This is something: ", something)

print("content completed")
"""
