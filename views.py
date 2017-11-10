#!/usr/bin/env python3
import feedparser
from html.parser import HTMLParser
import requests
from flask import Flask, render_template, flash, request
#from app import app
from mediumParserV2Test import  *

app = Flask(__name__)

user = ''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global user

    project = {'name' : 'ParseMe'}
    blog_titles = []

    if request.method == 'GET':
        return render_template('index.html',
                               project=project)


    elif request.method == 'POST':
        print("grabbing titles...")
        converted = dict(request.form)

        if 'first' in converted.keys(): # and len(request.form['checker']) == 0:

            username = request.form['username']
            user_titles = request.form.getlist("titles")
            userProfile = feedparser.parse('https://medium.com/feed/@{}'.format(username))

            for title in userProfile.entries:
                blog_titles.append(title.title)

            if len(blog_titles) == 0:
                return ("No titles found"), 404

            user += request.form['username']
            print("titles found!")
            return render_template('index.html',
                                   project=project,
                                   blog_titles=blog_titles)



        elif 'second' in converted.keys():
            print("start word search")
            words = converted['words']
            words = ''.join(words)
            if len(words) > 1:


                words = words.split(', ')
            selectedTitles = ''
            for k, v in converted.items():
                if k == 'check':
                    selectedTitles = v

            # begin parsing
            feed = access_profile(user)
            titles = generate_titles(feed)
            chosen = choose_title(selectedTitles, titles)

            word_search = generate_content(chosen, words)
            user = ''
            print("words found! ")
            return render_template('index.html',
                                   project=project,
                                   blog_titles=blog_titles,
                                   word_search=word_search)

if __name__ == '__main__':
    app.run(debug=True)
