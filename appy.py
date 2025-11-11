from flask import Flask, render_template, redirect, url_for, flash, request
import requests

app = Flask(__name__)
app.secret_key = 'Tu clave secreta'
API = 'https://pokeapi.co/api/v2/pokemon/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar_pokemon():

    pokemon_name = request.form.get('pokemon_name', '').strip().lower()


    if not pokemon_name:
        flash('Por favor, ingresa el nombre de un Pokémon.')
        return redirect(url_for('index'))
    
    try:
        response = requests.get(f'{API}{pokemon_name}')
        if response.status_code == 200:
            pokemon_data = response.json()
            return render_template('pokemon.html', pokemon=pokemon_data)
        else:
            flash('Pokémon no encontrado. Intenta con otro nombre o ID.')
            return redirect(url_for('index'))
    
    except requests.exceptions.RequestException as e:
        flash(f'Hubo un error al intentar obtener los datos del Pokémon: {e}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
