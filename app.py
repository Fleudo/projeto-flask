from flask import Flask, request, jsonify, render_template
import requests
import os
import qrcode
from io import BytesIO
from base64 import b64encode
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

data_url = "https://api.gwmcarclub.com.br/api/associates"

def fetch_associate_by_id(token, associate_id):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(f"{data_url}/{associate_id}", headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            if 'data' in data:
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
        qr_data = f"Nome: {associate['attributes']['name']}\nCPF: {associate['attributes']['cpf']}\nModelo do Carro: {associate['attributes']['car_model']}"
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_img = b64encode(buffer.getvalue()).decode('utf-8')
        return render_template('carteirinha.html', associate=associate['attributes'], qr_img=qr_img)
    else:
        return render_template('carteirinha.html', error='Pessoa inexistente na base de dados do clube')

if __name__ == '__main__':
    app.run(debug=True)
