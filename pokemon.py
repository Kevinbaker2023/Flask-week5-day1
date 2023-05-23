from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/")
def greeting():
    return 'Welcome to Pokemon!'

@app.route('/poke', methods=['GET', 'POST'])
def poke():
    if request.method == 'POST':
        new_pokemon = request.form.get('new_pokemon')
        print(new_pokemon)

        url = f'https://pokeapi.co/api/v2/pokemon/{new_pokemon}'
        response = requests.get(url)
        if response.ok:
            try:
                new_pokemon_data = response.json()
                pokemon_data = get_pokemon_data(new_pokemon_data)
                return render_template('poke.html', pokemon_data=pokemon_data)
            except IndexError:
                return 'That pokemon does not exist!'
    return render_template('poke.html')

def get_pokemon_data(data):
    pokemon_list = []
    new_pokemon = request.form.get('new_pokemon')
    url = f'https://pokeapi.co/api/v2/pokemon/{new_pokemon}'
    response = requests.get(url)
    new_pokemon_data = response.json()
    for new_pokemon in data:
            pokemon_dict = {
                 'name': f"{new_pokemon_data['forms'][0]['name']}",
                'ability': f"{new_pokemon_data['abilities'][0]['ability']['name']}",
                'experience': f"{new_pokemon_data['base_experience']}",
                'image': f"{new_pokemon_data['sprites']['front_shiny']}",
                'hp': f"{new_pokemon_data['stats'][0]['base_stat']}",
                'attack': f"{new_pokemon_data['stats'][1]['base_stat']}",
                'defense': f"{new_pokemon_data['stats'][2]['base_stat']}"
            }
            if len(pokemon_list) <= 0:
                pokemon_list.append(pokemon_dict)
    return pokemon_list