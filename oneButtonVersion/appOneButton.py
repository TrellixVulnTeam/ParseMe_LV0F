#!/usr/bin/env python3
import feedparser
from html.parser import HTMLParser
import requests
from flask import Flask, render_template, flash, request
#from app import app
from mediumParserV2Test import  *

app = Flask(__name__)


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

    if request.method == 'GET':
        return render_template('indexUpdate.html',
                               project=project)
    
    elif request.method == 'POST':

        username = request.form['username_input']
        selected_title = request.form['title_input']
        words = request.form['keyword_input']

        feed = access_profile(username)
        titles = generate_titles(feed)
        
        
        chosen_title = choose_title([selected_title], titles)

        #print("This is chosen! --> ", chosen)
        words = words.split(', ')
        word_search = generate_content(chosen_title, words)
        
        output = ''

        for k, v in word_search.items():
            output += "The phrase {} appears {} time(s) in the blog(s) selected.\n".format(
                k, v)

        #print("This is word_search: ", word_search)

        return render_template('indexUpdate.html',
                               project=project,
                               output=output)

if __name__ == '__main__':
    app.run(debug=True)
