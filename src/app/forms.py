from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length, ValidationError

from .models import User


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3,
                                                                          message='Username must be at least 3 characters long.'),
                                                   Regexp('^[A-Za-z0-9_]*$',
                                                          message='Username can only contain English letters, numbers, and underscores.')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,
                                                                            message='Password must be at least 8 characters long.')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        user = User.get_user_by('username', field.data)
        if user:
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        user = User.get_user_by('email', field.data)
        if user:
            raise ValidationError('Email already exists.')


class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
