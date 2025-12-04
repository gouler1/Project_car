from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User, Booking
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken.')

class BookingForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Book')

    def validate_end_date(self, end_date):
        if end_date.data < self.start_date.data:
            raise ValidationError('End date must be after start date.')
        if self.start_date.data < date.today():
            raise ValidationError('Start date cannot be in the past.')

class PaymentForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired()])
    expiry = StringField('Expiry (MM/YY)', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])
    submit = SubmitField('Pay')

class AddCarForm(FlaskForm):
    model = StringField('Model', validators=[DataRequired()])
    price_per_day = FloatField('Price per Day', validators=[DataRequired()])
    submit = SubmitField('Add Car')
