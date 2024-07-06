from flask import Flask, request, jsonify, render_template, url_for, send_file
import requests
import os
import qrcode
import json
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps

app = Flask(__name__)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

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
            data['data']['attributes']['id'] = associate_id
            return data['data']['attributes']
        except ValueError:
            return None
    else:
        return None

@app.route('/carteirinha/<int:associate_id>', methods=['GET'])
def carteirinha(associate_id):
    token = os.getenv("API_TOKEN")
    associate = fetch_associate_by_id(token, associate_id)
    if associate:
        qr_data = {
            "Número do Sócio": associate_id,
            "Nome": associate.get('nome', 'N/A'),
            "CPF": associate.get('cpf', 'N/A'),
            "Modelo do Carro": associate.get('carro_modelo', 'N/A'),
            "Versão": associate.get('carro_versao', 'N/A'),
            "Ano Modelo": associate.get('carro_anomodelo', 'N/A'),
            "Email": associate.get('email', 'N/A'),
            "Telefone": associate.get('telefone', 'N/A')
        }
        
        qr_data_json = json.dumps(qr_data, indent=4, ensure_ascii=False)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data_json)
        qr.make(fit=True)
        qr_img = qr.make_image(fill='black', back_color='white')

        # Cria a imagem da carteirinha
        card_width, card_height = 600, 350
        card_img = Image.new('RGB', (card_width, card_height), (255, 255, 255))
        draw = ImageDraw.Draw(card_img)
        font_path = "arial.ttf"  # Certifique-se de ter uma fonte TTF disponível
        bold_font_path = "arialbd.ttf"  # Fonte em negrito

        try:
            font = ImageFont.truetype(font_path, 18)
            bold_font = ImageFont.truetype(bold_font_path, 18)
            header_font = ImageFont.truetype(bold_font_path, 22)
        except IOError:
            font = ImageFont.load_default()
            bold_font = ImageFont.load_default()
            header_font = ImageFont.load_default()

        # Adiciona o fundo com opacidade reduzida
        background = Image.open('static/background.png').convert("RGBA")
        background = background.resize((card_width, card_height))
        background = Image.blend(background, Image.new("RGBA", background.size, (255, 255, 255, 0)), 0.4)  # Ajusta a opacidade
        card_img.paste(background, (0, 0), background)

        # Desenha os detalhes na carteirinha
        header_text = "Carteirinha de Sócio"
        header_width, header_height = draw.textsize(header_text, font=header_font)
        draw.text(((card_width - header_width) / 2, 20), header_text, font=header_font, fill='black', stroke_width=1)

        draw.text((20, 60), f"Nome: {associate['nome']}", font=bold_font, fill='black')
        draw.text((20, 90), f"Número do Sócio: {associate_id}", font=bold_font, fill='black')
        draw.text((20, 120), f"CPF: {associate['cpf']}", font=font, fill='black')
        draw.text((20, 150), f"Modelo do Carro: {associate['carro_modelo']}", font=font, fill='black')
        draw.text((20, 180), f"Versão: {associate['carro_versao']}", font=font, fill='black')
        draw.text((20, 210), f"Ano Modelo: {associate['carro_anomodelo']}", font=font, fill='black')
        draw.text((20, 240), f"Email: {associate['email']}", font=font, fill='red')
        draw.text((20, 270), f"Telefone: {associate['telefone']}", font=font, fill='red')

        # Adiciona o QR code na imagem da carteirinha
        qr_img = qr_img.resize((100, 100))
        card_img.paste(qr_img, (450, 120))

        # Arredonda os cantos
        radius = 20
        card_img = card_img.convert("RGBA")
        mask = Image.new("L", (card_width, card_height), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([(0, 0), (card_width, card_height)], radius=radius, fill=255)
        card_img.putalpha(mask)

        # Salva a imagem da carteirinha
        card_img_path = 'static/carteirinha.png'
        card_img.save(card_img_path)

        return send_file(card_img_path, mimetype='image/png')
    else:
        return "Pessoa inexistente na base de dados do clube", 404

if __name__ == '__main__':
    app.run(debug=True)
