from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignUpForm(FlaskForm):
	firstname = StringField('First Name', validators=[ DataRequired()])
	lastname = StringField('Last Name', validators=[ DataRequired()])
	email = StringField('E-mail', validators=[ DataRequired(), Email()])
	username = StringField('Username', validators=[ DataRequired(), Length(min=4)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')
	
class SignInForm(FlaskForm):
	username = StringField('Username', validators=[ DataRequired(), Length(min=4)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	submit = SubmitField('Sign In')

class NewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    newpage = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Add Page')