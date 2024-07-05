from flask import Flask, request, jsonify, render_template
import requests
import os
import qrcode
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
        qr = qrcode.make(f"ID: {associate_id}, Nome: {associate['attributes']['name']}, CPF: {associate['attributes']['cpf']}")
        qr.save('static/qr.png')
        return render_template('index.html', associate=associate['attributes'])
    else:
        return render_template('index.html', error='Pessoa inexistente na base de dados do clube')

if __name__ == '__main__':
    app.run(debug=True)
