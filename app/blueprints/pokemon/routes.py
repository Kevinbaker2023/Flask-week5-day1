from flask import request, render_template, flash, redirect, url_for
import requests
from app import db
from app.models import Pokemon, User
from app.blueprints.pokemon.forms import PokemonName
from flask_login import login_required, current_user
from . import pokemon

@pokemon.route("/")
@pokemon.route('/home', methods=['GET'])
def greeting():
    team = current_user.caught.all()
    return render_template('home.html', team=team)

@pokemon.route('/poke', methods=['GET', 'POST'])
@login_required
def poke():
    form = PokemonName()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = form.pokemon.data.lower()
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        response = requests.get(url)
        if response.ok:
                new_pokemon_data = response.json()
                pokemon_data = get_pokemon_data(new_pokemon_data)
                poke_data = {
                'pokemon_name': form.pokemon.data,
                'user_id': current_user.id
                }
                new_post = Pokemon()
                new_post.from_dict(poke_data)
                db.session.add(new_post)
                db.session.commit()
                return render_template('poke.html', pokemon_data=pokemon_data, form=form, poke_data=poke_data)
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

@pokemon.route('/catch/<string:pokemon_name>')
@login_required
def catch(pokemon_name):
    pokemon = Pokemon.query.filter_by(pokemon_name=pokemon_name).first()
    if pokemon:
        current_user.caught.append(pokemon)
        db.session.commit()
        flash(f"You successfully caught {pokemon_name.capitalize()}", 'success')
        return redirect (url_for('pokemon.greeting'))
    else:
        flash('You are not able to capture this pokemon!', 'danger')     
    return redirect(url_for('pokemon.greeting'))

@pokemon.route('/release/<int:pokemon_id>')
@login_required
def release(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        current_user.caught.remove(pokemon)
        db.session.commit()
        flash(f'You have successfully released your pokemon!', 'success')
        return redirect(url_for('pokemon.greeting'))
    else:
        flash('You are not able to release this Pokemon!', 'warning')
        return redirect(url_for('pokemon.greeting'))
    
@pokemon.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

@pokemon.route('/attack')
@login_required
def attack():
    return render_template('attack.html')