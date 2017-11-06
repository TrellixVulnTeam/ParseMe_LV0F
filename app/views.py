import feedparser
import logging
from html.parser import HTMLParser
import requests
from flask import render_template, flash
from app import app

#@app.context_processor
@app.route('/')
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
    userProfile = feedparser.parse('https://medium.com/feed/@joewmcdaniel')

    dog = 'hi how are you'
    return render_template('index.html',
                           project=project,
                           blogs=blogs,
                           dog=dog,
                           userProfile=userProfile)
