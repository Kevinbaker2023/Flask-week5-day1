from flask import request, render_template
import requests
from app.forms import PokemonName, LoginForm, SignupForm
from app import app

@app.route("/")
@app.route('/home')
def greeting():
    return 'Welcome to Pokemon!'

REGISTERED_USERS = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        if email in REGISTERED_USERS and password == REGISTERED_USERS[email]['password']:
            return f"Welcome {REGISTERED_USERS[email]['name']}!"
        else:
            return 'Email or password was incorrect, please try again.'
    else:
        return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.first_name.data + ' ' + form.last_name.data
        email = form.email.data.lower()
        password = form.password.data
        REGISTERED_USERS[email] = {
            'name': name,
            'password': password
        }
        print(REGISTERED_USERS)
        return 'Please proceed to login'
    else:
        return render_template('signup.html', form=form)

@app.route('/poke', methods=['GET', 'POST'])
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
            'move': f"{new_pokemon_data['moves'][16]['move']['name']}"
        }
        if len(pokemon_list) <= 0:
            pokemon_list.append(pokemon_dict)
    return pokemon_list