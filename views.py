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

    project = {'name' : 'UNICORN AI BLOG CHECKER'}
    blog_titles = []

    if request.method == 'GET':
        return render_template('index.html',
                               project=project)

    
    elif request.method == 'POST':

        print("The immutable multi dict request form ", request.form, "\n")

        converted = dict(request.form)
        print("This is converted to dict: ", converted, "\n")


        if 'first' in converted.keys(): # and len(request.form['checker']) == 0:
            print('\n\n test1 entered \n\n')

            
            username = request.form['username']
            user_titles = request.form.getlist("titles")
            userProfile = feedparser.parse('https://medium.com/feed/@{}'.format(username))

            for title in userProfile.entries:
                blog_titles.append(title.title)

            if len(blog_titles) == 0:
                return ("No titles found"), 404

            print("titles", user_titles)
            print('\n\n\n YAY \n\n\n')

            user += request.form['username']

            return render_template('index.html',
                                   project=project,
                                   blog_titles=blog_titles)



        elif 'second' in converted.keys():
            print('\n\n test2 entered \n\n')

            words = converted['words']
            words = ''.join(words)
            print("words after the join: ", words)
            if len(words) > 1:
                
                
                words = words.split(', ')
            #infoDict = dict(request.form)
            #print("This is blog content: ", blog_content)
            print("This is the mother fucking dict: ", converted)
            selectedTitles = ''
            print("before loop")
            for k, v in converted.items():
                if k == 'check':
                    selectedTitles = v
                    #print("here are the selected titles: ", v)
            # begin parsing
            print("before feed")
            feed = access_profile(user)
            titles = generate_titles(feed)
            #print(titles)
            #print("This is selected ", selectedTitles)
            chosen = choose_title(selectedTitles, titles)
            #print("This is chosen ", chosen)

            
            #print('Yay: ', request.form['checker'])
            word_search = None
            #words = words.split(', ')
            print("This is words: ", words)
            print("Right before word search")
            word_search = generate_content(chosen, words)
            search_collection = ''
            if word_search:
                for k, v in word_search.items():
                    search_collection += 'The phrase "{}" appears "{}" time(s) in the blog(s) selected.ð'.format(k, v)
            search_collection = search_collection.split('ð')
            #print("This is search_collection: ",search_collection)
            #print("This is the search_collection: ", search_collection)
            user = ''
            return render_template('index.html',
                                   project=project,
                                   blog_titles=blog_titles,
                                   search_collection=search_collection)

if __name__ == '__main__':
    app.run(debug=True)
