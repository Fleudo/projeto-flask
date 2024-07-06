import os
import requests
from flask import Flask, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont, ImageOps
import qrcode

app = Flask(__name__)

data_url = "https://api.gwmcarclub.com.br/api/associates"
api_token = os.getenv("API_TOKEN")

def add_rounded_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

@app.route("/carteirinha/<int:id>")
def carteirinha(id):
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(f"{data_url}/{id}", headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    data = response.json()
    associate = data.get("data", {}).get("attributes", {})

    try:
        # Tamanho da carteirinha
        card_width, card_height = 850, 550

        background_image = Image.open("static/background.png").convert("RGBA")
        background_image = background_image.resize((card_width, card_height))
        
        # Tornando o background menos vivo
        background_image = Image.blend(background_image, Image.new('RGBA', background_image.size, (255,255,255,0)), 0.25)

        draw = ImageDraw.Draw(background_image)

        font_path = "static/Arial.ttf"
        bold_font_path = "static/Arial-Bold.ttf"

        header_font_size = 36
        header_font = ImageFont.truetype(bold_font_path, header_font_size)
        header_text = "Carteirinha de Sócio"
        header_bbox = draw.textbbox((0, 0), header_text, font=header_font)
        header_width = header_bbox[2] - header_bbox[0]
        header_height = header_bbox[3] - header_bbox[1]
        draw.text(
            ((card_width - header_width) / 2, 20),
            header_text,
            font=header_font,
            fill="black"
        )

        font_size = 24
        bold_font_size = 24
        font = ImageFont.truetype(font_path, font_size)
        bold_font = ImageFont.truetype(bold_font_path, bold_font_size)

        offset = 100  # Dobrando o espaço do cabeçalho
        line_height = font_size + 10  # Aumentando o espaçamento entre linhas

        fields = [
            ("Nome:", associate.get("nome", "N/A")),
            ("Número do Sócio:", str(id)),
            ("CPF:", associate.get("cpf", "N/A")),
            ("Modelo do Carro:", associate.get("carro_modelo", "N/A")),
            ("Versão:", associate.get("carro_versao", "N/A")),
            ("Ano Modelo:", associate.get("carro_anomodelo", "N/A")),
        ]

        for field in fields:
            if "Nome" in field[0] or "Número do Sócio" in field[0]:
                draw.text((50, offset), f"{field[0]} {field[1]}", font=bold_font, fill="black")
            else:
                draw.text((50, offset), f"{field[0]} {field[1]}", font=font, fill="black")
            offset += line_height

        # Posicionando email e telefone
        email_text = f"Email: {associate.get('email', 'N/A')}"
        telefone_text = f"Telefone: {associate.get('telefone', 'N/A')}"
        
        email_bbox = draw.textbbox((0, 0), email_text, font=font)
        telefone_bbox = draw.textbbox((0, 0), telefone_text, font=font)
        email_width = email_bbox[2] - email_bbox[0]
        email_height = email_bbox[3] - email_bbox[1]
        telefone_width = telefone_bbox[2] - telefone_bbox[0]
        telefone_height = telefone_bbox[3] - telefone_bbox[1]

        draw.text((50, card_height - email_height - 20), email_text, font=font, fill="red")
        draw.text((card_width - telefone_width - 50, card_height - telefone_height - 20), telefone_text, font=font, fill="red")

        # Gerando QRCode com dados em JSON
        qr_data = {
            "Nome": associate.get("nome", "N/A"),
            "CPF": associate.get("cpf", "N/A"),
            "Modelo do Carro": associate.get("carro_modelo", "N/A"),
            "Versão": associate.get("carro_versao", "N/A"),
            "Ano Modelo": associate.get("carro_anomodelo", "N/A"),
            "Email": associate.get("email", "N/A"),
            "Telefone": associate.get("telefone", "N/A")
        }
        qr_code_image = qrcode.make(qr_data)
        qr_code_path = "static/qr_code.png"
        qr_code_image.save(qr_code_path)

        qr_code = Image.open(qr_code_path)
        qr_code_size = (150, 150)  # Aumentado em 15%
        qr_code = qr_code.resize(qr_code_size)
        qr_code_position = (card_width - qr_code_size[0] - 30, (card_height - qr_code_size[1]) // 2)
        background_image.paste(qr_code, qr_code_position)

        output_path = f"static/carteirinha_{id}.png"

        # Adicionando cantos arredondados
        background_image = add_rounded_corners(background_image, 50)
        background_image.save(output_path)

        return send_file(output_path, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
