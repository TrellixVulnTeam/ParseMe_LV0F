from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    project = {'name' : 'UNICORN AI BLOG CHECKER'}
    blogs = [ #MACHINE LEARNING AT WORK!!
        {
            'author' : {'username' : 'THE ZUCC'},
            'body' : 'Hello, fellow Human Beings. Have you tried VR?'
        },
        {
            'author' : {'username' : 'Joe'},
            'body' : 'give me the Z U C C'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           project=project,
                           blogs=blogs)
