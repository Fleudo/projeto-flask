from flask import Flask, request, jsonify, send_file
import requests
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Carregar variáveis de ambiente
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://api.gwmcarclub.com.br/api/associates"

@app.route('/carteirinha/<int:id>', methods=['GET'])
def carteirinha(id):
    try:
        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }
        response = requests.get(f"{API_URL}/{id}", headers=headers)
        response.raise_for_status()
        data = response.json()
        
        associate = data['data']['attributes']

        # Gerar dados do QR code
        qr_data = f"Nome: {associate.get('nome', 'N/A')}\n" \
                  f"CPF: {associate.get('cpf', 'N/A')}\n" \
                  f"Modelo do Carro: {associate.get('carro_modelo', 'N/A')}\n" \
                  f"Versão: {associate.get('carro_versao', 'N/A')}\n" \
                  f"Ano Modelo: {associate.get('carro_anomodelo', 'N/A')}\n" \
                  f"Email: {associate.get('email', 'N/A')}\n" \
                  f"Telefone: {associate.get('telefone', 'N/A')}"

        # Gerar QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Abrir imagem de fundo
        card = Image.open("static/background.png")
        draw = ImageDraw.Draw(card)

        # Carregar fontes
        try:
            font_path = "arial.ttf"  # Certifique-se de que o arquivo da fonte está disponível
            header_font = ImageFont.truetype(font_path, 40)
            text_font = ImageFont.truetype(font_path, 20)
        except IOError:
            # Fallback para uma fonte padrão caso a fonte especificada não esteja disponível
            header_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Adicionar cabeçalho
        header_text = "Carteirinha de Sócio"
        header_width, header_height = draw.textbbox((0, 0), header_text, font=header_font)[2:]
        header_x = (card.width - header_width) // 2
        draw.text((header_x, 20), header_text, font=header_font, fill="black")

        # Adicionar dados do associado
        text_y = 100
        text_spacing = 30

        draw.text((50, text_y), f"Nome: {associate.get('nome', 'N/A')}", font=text_font, fill="black")
        text_y += text_spacing
        draw.text((50, text_y), f"Número do Sócio: {id}", font=text_font, fill="black")
        text_y += text_spacing
        draw.text((50, text_y), f"CPF: {associate.get('cpf', 'N/A')}", font=text_font, fill="black")
        text_y += text_spacing
        draw.text((50, text_y), f"Modelo do Carro: {associate.get('carro_modelo', 'N/A')}", font=text_font, fill="black")
        text_y += text_spacing
        draw.text((50, text_y), f"Versão: {associate.get('carro_versao', 'N/A')}", font=text_font, fill="black")
        text_y += text_spacing
        draw.text((50, text_y), f"Ano Modelo: {associate.get('carro_anomodelo', 'N/A')}", font=text_font, fill="black")
        text_y += text_spacing
        draw.text((50, text_y), f"Email: {associate.get('email', 'N/A')}", font=text_font, fill="red")
        text_y += text_spacing
        draw.text((50, text_y), f"Telefone: {associate.get('telefone', 'N/A')}", font=text_font, fill="red")

        # Adicionar QR code à imagem
        qr_x = card.width - qr_img.size[0] - 20
        qr_y = (card.height - qr_img.size[1]) // 2
        card.paste(qr_img, (qr_x, qr_y))

        # Salvar imagem final
        card.save("static/carteirinha.png")

        return send_file("static/carteirinha.png", mimetype='image/png')

    except Exception as e:
        print(f"Error generating card: {e}")
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(debug=True)
