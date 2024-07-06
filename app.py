from flask import Flask, jsonify, send_file, render_template
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import requests
import json
import os

app = Flask(__name__)

# Carregar variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

API_URL = "https://api.gwmcarclub.com.br/api/associates"
API_TOKEN = os.getenv('API_TOKEN')

@app.route('/carteirinha/<int:associate_id>', methods=['GET'])
def carteirinha(associate_id):
    try:
        # Fazendo a solicitação à API
        headers = {'Authorization': f'Bearer {API_TOKEN}'}
        response = requests.get(f'{API_URL}/{associate_id}', headers=headers)
        response_data = response.json()

        if response.status_code != 200 or 'data' not in response_data:
            return "Erro ao obter dados do associado", 404

        associate = response_data['data']['attributes']
        qr_data = json.dumps({
            "Nome": associate.get('nome', 'N/A'),
            "Número do Sócio": associate_id,
            "CPF": associate.get('cpf', 'N/A'),
            "Modelo do Carro": associate.get('carro_modelo', 'N/A'),
            "Versão": associate.get('carro_versao', 'N/A'),
            "Ano Modelo": associate.get('carro_anomodelo', 'N/A'),
            "Email": associate.get('email', 'N/A'),
            "Telefone": associate.get('telefone', 'N/A')
        })

        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')

        card_width, card_height = 800, 400
        card = Image.new('RGBA', (card_width, card_height), (255, 255, 255, 0))

        try:
            background = Image.open('static/background.png').convert('RGBA')
            background = background.resize((card_width, card_height))
            card.paste(background, (0, 0))
        except FileNotFoundError:
            pass

        draw = ImageDraw.Draw(card)
        font_path = "arial.ttf"

        try:
            header_font = ImageFont.truetype(font_path, 40)
            main_font = ImageFont.truetype(font_path, 24)
            bold_font = ImageFont.truetype(font_path, 24)
        except IOError:
            header_font = ImageFont.load_default()
            main_font = ImageFont.load_default()
            bold_font = ImageFont.load_default()

        header_text = "Carteirinha de Sócio"
        header_width, header_height = draw.textsize(header_text, font=header_font)
        draw.text(((card_width - header_width) / 2, 20), header_text, font=header_font, fill='black')

        info_text = [
            f"Nome: {associate.get('nome', 'N/A')}",
            f"Número do Sócio: {associate_id}",
            f"CPF: {associate.get('cpf', 'N/A')}",
            f"Modelo do Carro: {associate.get('carro_modelo', 'N/A')}",
            f"Versão: {associate.get('carro_versao', 'N/A')}",
            f"Ano Modelo: {associate.get('carro_anomodelo', 'N/A')}",
            f"Email: {associate.get('email', 'N/A')}",
            f"Telefone: {associate.get('telefone', 'N/A')}"
        ]

        y_offset = 80
        for line in info_text:
            if "Nome" in line or "Número do Sócio" in line:
                font = bold_font
            else:
                font = main_font
            draw.text((20, y_offset), line, font=font, fill='black' if 'Email' not in line and 'Telefone' not in line else 'red')
            y_offset += 30

        qr_size = 150
        qr_img = qr_img.resize((qr_size, qr_size))
        card.paste(qr_img, (card_width - qr_size - 20, card_height - qr_size - 20))

        # Salvar a carteirinha como imagem
        card_path = 'static/carteirinha.png'
        card.save(card_path)

        # Retornar a carteirinha como resposta
        return send_file(card_path, mimetype='image/png')

    except Exception as e:
        return f"Error generating card: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
