from flask import request, render_template, redirect, url_for, flash
import requests
from app.forms import PokemonName, LoginForm, SignupForm
from app import app, db
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import current_user, login_user, logout_user, login_required

@app.route("/")
@app.route('/home')
def greeting():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f"Welcome {queried_user.first_name}. You successfully logged in!", 'secondary')
            return redirect(url_for('poke'))
        else:
            error = 'Email or password was incorrect, please try again!'
            return render_template('login.html' , form=form, error=error)
    else:
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
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
        
        flash(f"Thank you for signing up {user_data['first_name']}, please login!", 'secondary')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)
    
@app.route('/logout')
def logout():
    logout_user()
    flash(f"You have successfully logged out", 'danger')
    return redirect(url_for('login'))

    

@app.route('/poke', methods=['GET', 'POST'])
@login_required
def poke():
    form = PokemonName()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = form.pokemon.data.lower()
        print(pokemon)
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        response = requests.get(url)
        if response.ok:
                try:
                    new_pokemon_data = response.json()
                    pokemon_data = get_pokemon_data(new_pokemon_data)
                    return render_template('poke.html',pokemon_data=pokemon_data, form=form)
                except IndexError:
                     return 'That pokemon does not exist!'
    return render_template('poke.html', form=form)

def get_pokemon_data(data):
    pokemon_list = []
    pokemon = request.form.get('pokemon')
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
    response = requests.get(url)
    new_pokemon_data = response.json()
    for pokemon in data:
        pokemon_dict = {
            'name': f"{new_pokemon_data['forms'][0]['name']}",
            'ability': f"{new_pokemon_data['abilities'][0]['ability']['name']}",
            'experience': f"{new_pokemon_data['base_experience']}",
            'image': f"{new_pokemon_data['sprites']['front_shiny']}",
            'hp': f"{new_pokemon_data['stats'][0]['base_stat']}",
            'attack': f"{new_pokemon_data['stats'][1]['base_stat']}",
            'defense': f"{new_pokemon_data['stats'][2]['base_stat']}",
            'move': f"{new_pokemon_data['moves'][16]['move']['name']}",
            'type1': f"{new_pokemon_data['types'][0]['type']['name']}",
        }
        if len(pokemon_list) <= 0:
            pokemon_list.append(pokemon_dict)
    return pokemon_list