from flask import Flask, request, jsonify, render_template
import requests
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

data_url = "https://api.gwmcarclub.com.br/api/associates"

def fetch_associate_by_id(token, associate_id):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    print(f"Token: {token}")  # Debugging
    print(f"Fetching associate with ID: {associate_id}")  # Debugging
    response = requests.get(f"{data_url}/{associate_id}", headers=headers)
    print(f"Response status code: {response.status_code}")  # Debugging
    print(f"Response text: {response.text}")  # Debugging
    
    if response.status_code == 200:
        try:
            data = response.json()
            if 'data' in data:
                print(f"Data found: {data['data']}")  # Debugging
                return data['data']
            else:
                return None
        except ValueError:
            return None
    else:
        return None

@app.route('/verify/<int:associate_id>', methods=['GET'])
def verify(associate_id):
    token = os.getenv("API_TOKEN")
    print(f"Token: {token}")  # Debugging
    associate = fetch_associate_by_id(token, associate_id)
    if associate:
        return render_template('index.html', associate=associate['attributes'])
    else:
        return render_template('index.html', error='Pessoa inexistente na base de dados do clube')

if __name__ == '__main__':
    print("Starting Flask application..."
    app.run(debug=True)
