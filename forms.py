from flask_wtf import FlaskForm 
from wtforms import Form, StringField, PasswordField,  validators, SubmitField, SelectField, IntegerField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo, Length
from models import User
from passlib.hash import pbkdf2_sha256


def invalid_credentials(form, field):
    """ Username and password checker """
    username_entered = form.username.data
    password_entered = field.data

    # Check credentials are valid.
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")

class RegistrationForm(FlaskForm):
    """User Signup Form"""

    username = StringField('Username', validators=[InputRequired(message="Username required"), Length(min=4, max=15, message="Username must be between four and fifteen characters")])
    password = PasswordField("Password", validators=[InputRequired(message="Password required"), Length(min=6, max=15, message="Password must be between 6-15 characters")])
    confirmPassword = PasswordField("Repeat password", validators=[InputRequired(message="Password required"), EqualTo('password', message="Passwords must match")])
    website = StringField("Website")
    submit = SubmitField("Register")


    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists select another name")


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Username', validators=[InputRequired(message="Username required.")])
    password = PasswordField("Password", validators=[InputRequired(message="Password required."), invalid_credentials])
    submit = SubmitField("Login")

def choice_query():
    return Choice.query

class SearchForm(FlaskForm):
    """Search Form"""

    isbn = StringField('ISBN')
    title = StringField('Title')
    author = StringField('Name')
    year = StringField('Year')
    search = StringField('Input')
    book_search = SelectField(choices=[('isbn', 'isbn'), ('title', 'title'), ('author', 'author') ])
    submit = SubmitField('BUTTON')

class ReviewForm(FlaskForm):
    score = IntegerField("Review rating", validators=[Length(min=1, max=1, message="one digit between 0 and 5")])
    user_review = StringField("Short review of book")
    submit = SubmitField("Submit")




    
   

  






    

