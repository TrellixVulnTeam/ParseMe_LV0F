import feedparser
import logging
from html.parser import HTMLParser
import requests
from flask import render_template, flash, request
from app import app


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    project = {'name' : 'UNICORN AI BLOG CHECKER'}
    blogs = [ #MACHINE LEARNING AT WORK!!
        {
            'author' : {'username' : 'THE ZUCC'},
            'blogtitle' : 'LIVE FROM MENLO PARK',
            'body' : 'Hello, fellow Human Beings. Have you tried VR?'
        },
        {
            'author' : {'username' : 'Joe'},
            'blogtitle' : 'HIRE ME',
            'body' : 'give me the Z U C C'
        }
    ]
    blog_title = []
    blog_content = []

    if request.method == 'POST':
        username = request.form['username']
        user_titles = request.form.getlist("titles")
        userProfile = feedparser.parse('https://medium.com/feed/@{}'.format(username))

        for title in userProfile.entries:
            blog_title.append(title.title)
        if len(blog_title) == 0:
                return ("No titles found")

        for content in userProfile.entries:
            blog_content.append(content.content)

    return render_template('index.html',
                           project=project,
                           blog_title=blog_title,
                           blog_content=blog_content)
