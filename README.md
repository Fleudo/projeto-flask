# projeto-flask# Aplicativo Flask para Verificação de Associados

Este aplicativo Flask permite a verificação de associados em uma base de dados remota via uma API REST. Ele utiliza Flask para a interface web e se integra com uma API para buscar informações dos associados.

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- Conta no GitHub
- Conta no Render.com para deploy

## Dependências

Crie um arquivo `requirements.txt` com o seguinte conteúdo:

```
Flask
requests
gunicorn
python-dotenv
```

## Estrutura do Projeto

```
Projeto/
│
├── app.py
├── requirements.txt
├── Procfile
├── .env
└── templates/
    └── index.html
```

## Arquivos

### `app.py`

```python
from flask import Flask, request, jsonify, render_template
import requests
import os
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

if __name__ == '__main__':
    app.run(debug=True)
```

### `requirements.txt`

```
Flask
requests
gunicorn
python-dotenv
```

### `Procfile`

```
web: gunicorn app:app
```

### `.env`

```
API_TOKEN=seu-token-aqui
```

### `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verificação do Associado</title>
</head>
<body>
    <h1>Verificação do Associado</h1>
    {% if associate %}
        <p>Nome: {{ associate.nome }}</p>
        <p>CPF: {{ associate.cpf }}</p>
        <p>Modelo do Carro: {{ associate.carro_modelo }}</p>
        <p>Versão: {{ associate.carro_versao }}</p>
        <p>Ano Modelo: {{ associate.carro_anomodelo }}</p>
        <p>Email: {{ associate.email }}</p>
        <p>Telefone: {{ associate.telefone }}</p>
    {% else %}
        <p>{{ error }}</p>
    {% endif %}
</body>
</html>
```

## Executando o Aplicativo Localmente

1. Clone o repositório.
2. Navegue até o diretório do projeto.
3. Instale as dependências: `pip install -r requirements.txt`
4. Execute o aplicativo: `flask run`

## Deploy no Render.com

1. Conecte sua conta do GitHub ao Render.com.
2. Crie um novo projeto e selecione o repositório do GitHub.
3. Defina as variáveis de ambiente conforme o arquivo `.env`.
4. Configure o build e o start command: `pip install -r requirements.txt` e `gunicorn app:app`.
5. Deploy o aplicativo.

Esta documentação cobre a configuração e implantação básica do aplicativo Flask para verificação de associados. Para mais detalhes sobre Flask ou sobre como personalizar seu aplicativo, consulte a [documentação do Flask](https://flask.palletsprojects.com/).
