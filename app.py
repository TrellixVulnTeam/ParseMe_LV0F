#!/usr/bin/env python3
import feedparser
from html.parser import HTMLParser
import requests
from flask import Flask, render_template, flash, request
from mediumParserV2 import *

app = Flask(__name__)
user = ''


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Main Page
    """

    global user

    project = {'name': 'UNICORN AI BLOG CHECKER'}
    blog_titles = []

    # When the page is first visited
    if request.method == 'GET':
        return render_template('index.html',
                               project=project)

    # One of the find buttons has been used
    elif request.method == 'POST':

        # Convert Immutable multi dict from request.form to
        # a dictionary so that key and values to be accessed
        converted = dict(request.form)

        # First find button clicked
        if 'first' in converted.keys():

            # Retrieves username value from form
            username = request.form['username']

            # RSS feed of user profile
            feed = access_profile(username)

            # Dictionary of blog titles with profile
            blog_titles = generate_titles(feed).keys()

            if len(blog_titles) == 0:
                blog_titles = ["No titles found!"]

            # This is how the username is retained for the next submit button!
            # A global variable is used
            # ...in the future this may not be needed with ajax implemented
            user += request.form['username']

            return render_template('index.html',
                                   project=project,
                                   blog_titles=blog_titles)

        # Second find button clicked
        elif 'second' in converted.keys():

            # Retrieve the words entered from
            # the key 'words' in the converted form dict
            words = converted['words']

            # convert list of words into string
            words = ''.join(words)

            # seperate words back into a list to be parsed
            words = words.split(', ')

            # selectedTitles is a list of titles in the converted form dict
            selectedTitles = ''
            for k, v in converted.items():
                if k == 'check':
                    selectedTitles = v

            # --- Use mediumParser here ---

            # Access feed
            feed = access_profile(user)

            # Generate a dict of all user titles with links to be referenced
            titles = generate_titles(feed)

            # Generate a dict of chosen titles and
            # links based on what titles are selected
            chosen = choose_title(selectedTitles, titles)

            # Generate a dict of words and the times they appear in the blog(s)
            word_search = None
            word_search = generate_content(chosen, words)

            # --- End mediumParser usage ---

            # Refresh global user reference to username
            user = ''

            return render_template('index.html',
                                   project=project,
                                   blog_titles=blog_titles,
                                   word_search=word_search)


if __name__ == '__main__':
    app.run(debug=True)
