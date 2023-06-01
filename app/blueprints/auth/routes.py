from flask import request, render_template, redirect, url_for, flash
from app.blueprints.auth.forms import LoginForm, SignupForm
from app import db
from . import auth
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f"Welcome {queried_user.first_name}. You successfully logged in!", 'primary')
            return redirect(url_for('pokemon.poke'))
        else:
            error = 'Email or password was incorrect, please try again!'
            return render_template('login.html' , form=form, error=error)
    else:
        return render_template('login.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'email': form.email.data.lower(),
            'password': form.password.data
        }

        new_user = User()
        new_user.from_dict(user_data)
        db.session.add(new_user)
        db.session.commit()
        
        flash(f"Thank you for signing up {user_data['first_name']}, please login!", 'primary')
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=form)
    
@auth.route('/logout')
def logout():
    logout_user()
    flash(f"You have successfully logged out", 'danger')
    return redirect(url_for('auth.login'))