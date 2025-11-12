from flask import Flask, render_template, redirect, url_for, flash, request
import requests

app = Flask(__name__)
app.secret_key = 'Tu_clave_secreta_aqui'
API = 'https://pokeapi.co/api/v2/pokemon/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar_pokemon():
    pokemon_name = request.form.get('pokemon_name', '').strip().lower()

    if not pokemon_name:
        flash('Por favor, ingresa el nombre de un Pokémon', 'error')
        return redirect(url_for('index'))
    
    try:
        response = requests.get(f'{API}{pokemon_name}')
        if response.status_code == 200:
            pokemon_data = response.json()

            pokemon_info = {
                'name': pokemon_data['name'].capitalize(),
                'id': pokemon_data['id'],
                'height': pokemon_data['height'] / 10, 
                'weight': pokemon_data['weight'] / 10,  
                'image': pokemon_data['sprites']['front_default'],
                'types': [t['type']['name'] for t in pokemon_data['types']],
                'abilities': [a['ability']['name'].capitalize() for a in pokemon_data['abilities']]
            }

            return render_template('pokemon.html', pokemon=pokemon_info)
        else:
            flash('Pokémon no encontrado. Intenta con otro nombre o ID.', 'error')
            return redirect(url_for('index'))
    
    except requests.exceptions.RequestException as e:
        flash('Error al buscar el pokemon', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
