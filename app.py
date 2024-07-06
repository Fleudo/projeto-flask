from flask import Flask, render_template, send_file
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import requests

app = Flask(__name__)

data_url = "https://api.gwmcarclub.com.br/api/associates"

@app.route('/carteirinha/<int:associate_id>', methods=['GET'])
def carteirinha(associate_id):
    try:
        token = os.getenv("API_TOKEN")
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f"{data_url}/{associate_id}", headers=headers)
        response.raise_for_status()
        data = response.json()

        associate = data.get('data', {}).get('attributes', {})
        nome = associate.get('nome', 'N/A')
        cpf = associate.get('cpf', 'N/A')
        carro_modelo = associate.get('carro_modelo', 'N/A')
        carro_versao = associate.get('carro_versao', 'N/A')
        carro_anomodelo = associate.get('carro_anomodelo', 'N/A')
        email = associate.get('email', 'N/A')
        telefone = associate.get('telefone', 'N/A')

        qr_data = {
            "Nome": nome,
            "CPF": cpf,
            "Modelo do Carro": carro_modelo,
            "Versão": carro_versao,
            "Ano Modelo": carro_anomodelo,
            "Email": email,
            "Telefone": telefone
        }
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr_code.add_data(qr_data)
        qr_code.make(fit=True)
        qr_img = qr_code.make_image(fill_color="black", back_color="white")
        qr_path = os.path.join("static", "qr_code.png")
        qr_img.save(qr_path)

        background_path = os.path.join("static", "background_image.png")
        card = Image.open(background_path)
        draw = ImageDraw.Draw(card)
        font_path = os.path.join("static", "arial.ttf")
        font_size = 20
        font = ImageFont.truetype(font_path, font_size)
        header_font = ImageFont.truetype(font_path, font_size + 10)
        bold_font = ImageFont.truetype(font_path, font_size)

        header_text = "Carteirinha de Sócio"
        header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
        header_width, header_height = header_bbox[2] - header_bbox[0], header_bbox[3] - header_bbox[1]
        draw.text(((card.width - header_width) / 2, 10), header_text, fill="black", font=header_font)

        draw.text((50, 50), f"Nome: {nome}", fill="black", font=bold_font)
        draw.text((50, 100), f"Número do Sócio: {associate_id}", fill="black", font=bold_font)
        draw.text((50, 150), f"CPF: {cpf}", fill="black", font=font)
        draw.text((50, 200), f"Modelo do Carro: {carro_modelo}", fill="black", font=font)
        draw.text((50, 250), f"Versão: {carro_versao}", fill="black", font=font)
        draw.text((50, 300), f"Ano Modelo: {carro_anomodelo}", fill="black", font=font)
        draw.text((50, 350), f"Email: {email}", fill="red", font=font)
        draw.text((50, 400), f"Telefone: {telefone}", fill="red", font=font)

        qr_code_img = Image.open(qr_path)
        card.paste(qr_code_img, (600, 300))

        card_path = os.path.join("static", "carteirinha.png")
        card.save(card_path)

        return send_file(card_path, mimetype='image/png')

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}", 500
    except Exception as e:
        return f"Error generating card: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
