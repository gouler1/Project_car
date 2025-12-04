from flask import render_template, redirect, url_for, flash, request
from app import app, db
from forms import LoginForm, RegisterForm, BookingForm, PaymentForm, AddCarForm
from models import User, Car, Booking
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/cars')
def cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)

@app.route('/car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    form = BookingForm()
    if form.validate_on_submit():
        # Проверка доступности: нет ли пересечений дат
        overlapping = Booking.query.filter(
            Booking.car_id == car_id,
            Booking.end_date >= form.start_date.data,
            Booking.start_date <= form.end_date.data
        ).first()
        if overlapping:
            flash('Car not available for these dates.')
            return redirect(url_for('car_detail', car_id=car_id))
        
        booking = Booking(
            user_id=current_user.id,
            car_id=car_id,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking created! Proceed to payment.')
        return redirect(url_for('payment', booking_id=booking.id))
    return render_template('car_detail.html', car=car, form=form)

@app.route('/payment/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user.id:
        flash('Access denied.')
        return redirect(url_for('index'))
    form = PaymentForm()
    if form.validate_on_submit():
        # Симуляция платежа
        booking.paid = True
        db.session.commit()
        flash('Payment successful! Booking confirmed.')
        return redirect(url_for('profile'))
    return render_template('car_detail.html', car=booking.car, form=form)  # Переиспользуем шаблон для простоты

@app.route('/profile')
@login_required
def profile():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', bookings=bookings)

@app.route('/admin', methods=['GET', 'POST'])
@login_required  # Для простоты, любой логин - админ; в реале добавь роль
def admin():
    form = AddCarForm()
    if form.validate_on_submit():
        car = Car(model=form.model.data, price_per_day=form.price_per_day.data)
        db.session.add(car)
        db.session.commit()
        flash('Car added!')
        return redirect(url_for('admin'))
    cars = Car.query.all()
    return render_template('admin.html', form=form, cars=cars)
