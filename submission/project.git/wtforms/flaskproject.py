from flask import Flask, render_template, url_for
from flaskform import Registration, Login
app = Flask(__name__)

app.config['SECRET_KEY'] = '8c6224d105d70346'

posts =[

{
	'author':'Lol1',
	'title':'Blog Post1',
	'content':'First content',
	'date_posted':'April 20, 2018'
},
{
	'author':'Lol2',
	'title':'Blog Post2',
	'content':'Second content',
	'date_posted':'June 21, 2018'
}


]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register')
def register():
	form = Registration()
	return render_template('register.html', title='Registration', form=form)

@app.route('/login')
def login():
	form = Login()
	return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)