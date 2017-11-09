#!/usr/bin/env python3
import feedparser
import requests
from flask import Flask, render_template, flash, request
from mediumParserV2Test import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    Main Page
    """

    project = {'name': 'UNICORN AI BLOG CHECKER'}

    # When the page is first visited
    if request.method == 'GET':
        return render_template('indexOneButton.html',
                               project=project)

    # Submit button entered
    elif request.method == 'POST':

        username = request.form['username_input']
        selected_title = request.form['title_input']
        words = request.form['keyword_input']
        words = words.split(', ')

        # Access feed
        feed = access_profile(username)

        # Generate a dict of all user titles with links to be referenced
        titles = generate_titles(feed)

        # Generate a dict of chosen titles and
        # links based on what titles are selected
        chosen_title = choose_title([selected_title], titles)

        # Generate a dict of words and the times they appear in the blog(s)
        word_search = generate_content(chosen_title, words)

        # The number of occurences word appears
        # in the blog(s) on the front end
        output = ''
        if word_search:
            for k, v in word_search.items():
                output += "The phrase {} appears {} \
                time(s) in the blog(s) selected.\n".format(k, v)

        return render_template('indexOneButton.html',
                               project=project,
                               output=output)


if __name__ == '__main__':
    app.run(debug=True)
