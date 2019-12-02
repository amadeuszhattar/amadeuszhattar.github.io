from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db
from flask_login import login_user, current_user, logout_user
from flaskblog.forms import RegistrationForm, LoginForm, UpdateForm, PostForm
from flaskblog.models import User, Post
import secrets
import os


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()    # displaying posts from the database           
    return render_template('home.html', posts=posts)


@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))   #checking if user is currently logged, if yes redirect them to home page when clicking on register button
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()                #putting data from forms into the database
        flash(f'Account has been created. You can log in now.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))    #checking if user is currently logged, if yes redirect them to home page when clicking on login button
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and form.password.data:      #if data from login forms is same as data in database user will be redirected and logged
            login_user(user)
            return redirect(url_for('home'))
        else:        
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


def save(form_picture):  #purpose of this is randomizing name of this image with random hex
    random_hex = secrets.token_hex(8)                     # base of a file name
    _, f_ext = os.path.splitext(form_picture.filename) #getting the extension of the imported picture
    file_picture = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures',file_picture) #joining full route all the way up to the package directory with static folder and pictures folder with filename
                #os.path.join makes sure that all of that gets contatenated correctly into one path
    form_picture.save(picture_path)
    return file_picture

@app.route("/ac", methods=['GET', 'POST'])
def ac():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save(form.picture.data)  
            current_user.image_file = picture_file   #setting user's profile picture
        current_user.username = form.username.data
        current_user.password = form.password.data
        db.session.commit()
        flash('Account has been updated','info')
        return redirect(url_for('ac')) #redirection here in used to avoid another POST request on reload
    elif request.method == 'GET':       #populating users form with user data
        form.username.data = current_user.username
        form.password.data = current_user.password
    image_file = url_for('static', filename='pictures/' + current_user.image_file)
    return render_template('ac.html', title='Your Account', image_file=image_file, form=form) 
                                                     #passing image file into ac template
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/new_post", methods=['GET', 'POST'])

def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post has been creted.", 'success')
        return redirect(url_for('home'))
    return render_template('new_post.html', title='New Post', legend='New Post', form=form)


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])

def update_post(post_id):
    post = Post.query.get(post_id)
    if post.author == current_user:      #only users that created their posts can access the update page
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data   #filling forms with current content/title of a post
            db.session.commit()
            flash('Post has been updated', 'info')
            return redirect(url_for('home'))

        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content

        return render_template('new_post.html', title='Updatew Post', legend='Update Post',form=form)
    else:
        return redirect(url_for('home'))


@app.route("/post/<int:post_id>/delete", methods=['POST'])

def delete_post(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted', 'info')
    return redirect(url_for('home'))
