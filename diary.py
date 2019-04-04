from flask import Flask, render_template, url_for, flash, redirect
from forms import SignUpForm, SignInForm, NewForm
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
    
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password =  db.Column(db.String(60), nullable=False)
    pages = db.relationship('Page', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"
posts = [
	{
		'title': 'First Day of College',
		'content': 'Lorem ipsum dolor sit amet, et appareat periculis has. Eam ea putent laoreet cotidieque. Ne sed nominati molestiae comprehensam, velit eripuit corpora no nec. Hendrerit reprimique quo ei, ad causae vocent saperet mei.',
		'date_posted': 'March 20, 2019'
	},
	{
		'title': 'Pressure of Homework',
		'content':'Quo simul facilisi intellegat ut, ius ex nulla choro expetenda. Vix exerci impetus nonumes eu, est sint hendrerit rationibus etVim saepe vocibus convenire inum repudiandae mel ei.',
		'date_posted': 'March 21, 2019'
	}
]

@app.route("/")
def home():
    return render_template('home.html')
	
@app.route("/myDiary")
@login_required
def myDiary():
    return render_template('myDiary.html', posts=posts)

@app.route("/addNew", methods=['GET', 'POST'])
@login_required
def addNew():
    form = NewForm()
    if form.validate_on_submit():
        flash('Posted!')
        return redirect(url_for('myDiary'))
    return render_template('addNew.html')

@app.route("/signIn", methods=['GET', 'POST'])
def signIn():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('myDiary'))
        else:
            flash('Invalid username and password!')
    return render_template('signIn.html', form=form)

@app.route("/signUp", methods=['GET', 'POST'])
def signUp():
    form = SignUpForm()
    if form.validate_on_submit():
        new_hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=new_hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('myDiary'))
    return render_template('signUp.html', form=form)
	

if __name__ == '__main__':
    app.run(debug=True)
