from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
import email_validator
from server.models import User, Binance_Info, Bot, Transaction


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=10)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already in use.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already in use.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=10)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    api_key = StringField('API KEY',
                           validators=[DataRequired(), Length(min=5, max=100)])
    api_secret = StringField('API SECRET KEY',
                           validators=[DataRequired(), Length(min=5, max=100)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already in use.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already in use.')



class ResetPasswordForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=10)])
    email = StringField('Email',
                    validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('There is no account with that username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')


class Transaction_DepositForm(FlaskForm):
    amount = IntegerField('Amount',
                          validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Deposit')

    def validate_amount(self, amount):
        if amount.data > 1000:
            raise ValidationError('You can only deposit 1000 at once.')


class BotForm(FlaskForm):
    api_key = StringField('API KEY',
                           validators=[DataRequired(), Length(min=5, max=100)])
    api_secret = StringField('API SECRET KEY',
                           validators=[DataRequired(), Length(min=5, max=100)])
    bot_id = IntegerField('Bot ID',
                           validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Update')

    def validate_api_key(self, api_key):
        if api_key.data == "-":
            raise ValidationError('Change API KEY.')

    def validate_api_secret(self, api_secret):
        if api_secret.data == "-":
            raise ValidationError('Change API SECRET KEY.')

    def validate_bot_id(self, bot_id):
        if bot_id.data != "-596127":
            raise ValidationError('Can\'t be changed.')