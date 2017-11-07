import feedparser
import logging
from html.parser import HTMLParser
import requests
from flask import render_template, flash, request
from app import app


user = ''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global user

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


    if request.method == 'GET':
        print("\n\n HOWDY \n\n")
        return render_template('index.html',
                               project=project)


    elif request.method == 'POST':
        if request.form["action"] == 'test1':
            username = request.form['username']
            user_titles = request.form.getlist("titles")
            userProfile = feedparser.parse('https://medium.com/feed/@{}'.format(username))
            for title in userProfile.entries:
                blog_title.append(title.title)
            if len(blog_title) == 0:
                return ("No titles found"), 404

            print("titles", user_titles)
            print('\n\n\n YAY \n\n\n')
            user += request.form['username']
            return render_template('index.html',
                                   project=project,
                                   blog_title=blog_title,
                                   blog_content=blog_content)



        elif request.form['action'] == 'zucc':
            print("hello")
            #for content in userProfile.entries:
            for content in request.form['check']:
                #print(request.form['check'])
                #print(request.form['check'])
                print("This is content: ", content)
                blog_content.append(content)
            for k, v in request.form.items():
                print("This is the key: ", k)
                print("This is the value: ",v)
            print("This is the username: ", user)
            user = ''
            return render_template('index.html',
                                   project=project,
                                   blog_title=blog_title,
                                   blog_content=blog_content)

    #return render_template('index.html',
    #project=project)
