from flask import Flask, request, jsonify, render_template
import requests
import os
import qrcode
from dotenv import load_dotenv
from io import BytesIO
from flask import send_file

app = Flask(__name__)

load_dotenv()

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
    associate = fetch_associate_by_id(token, associate_id)
    if associate:
        return render_template('index.html', associate=associate['attributes'])
    else:
        return render_template('index.html', error='Pessoa inexistente na base de dados do clube')

@app.route('/carteirinha/<int:associate_id>', methods=['GET'])
def carteirinha(associate_id):
    token = os.getenv("API_TOKEN")
    associate = fetch_associate_by_id(token, associate_id)
    if associate:
        qr_data = f"Nome: {associate['attributes'].get('name', 'N/A')}\nCPF: {associate['attributes'].get('cpf', 'N/A')}\nModelo do Carro: {associate['attributes'].get('car_model', 'N/A')}\nVersão: {associate['attributes'].get('car_version', 'N/A')}\nAno Modelo: {associate['attributes'].get('car_year_model', 'N/A')}\nEmail: {associate['attributes'].get('email', 'N/A')}\nTelefone: {associate['attributes'].get('phone', 'N/A')}"
        qr = qrcode.make(qr_data)
        qr_io = BytesIO()
        qr.save(qr_io, 'PNG')
        qr_io.seek(0)
        return send_file(qr_io, mimetype='image/png')
    else:
        return "Pessoa inexistente na base de dados do clube", 404

if __name__ == '__main__':
    app.run(debug=True)
