Aqui está o README atualizado para o seu projeto no GitHub:

---

# Projeto Flask Carteirinha de Sócio

Este projeto Flask gera carteirinhas de sócios com QRCode. A aplicação busca dados de um endpoint, gera uma imagem de carteirinha com um background customizado, insere os dados do sócio e adiciona um QRCode com informações em JSON.

## Estrutura do Projeto

```
Projeto/
├── static/
│   ├── Arial.ttf
│   ├── Arial-Bold.ttf
│   ├── background.png
│   ├── qr_code.png
│   └── carteirinha_<id>.png
├── templates/
├── .env
├── .gitignore
├── Procfile
├── app.py
└── requirements.txt
```

## Requisitos

- Python 3.8+
- Flask
- Pillow
- Requests
- qrcode

## Instalação

1. Clone o repositório:

```sh
git clone https://github.com/SeuUsuario/projeto-flask.git
cd projeto-flask
```

2. Crie um ambiente virtual:

```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Instale as dependências:

```sh
pip install -r requirements.txt
```

4. Adicione seu `API_TOKEN` no arquivo `.env`.

## Executando a Aplicação

1. Inicie o servidor Flask:

```sh
flask run
```

2. Acesse `http://127.0.0.1:5000/carteirinha/<id>` no navegador, onde `<id>` é o ID de um associado.

## Deploy no Render

1. Faça login no [Render](https://render.com/).
2. Crie um novo serviço web e conecte-o ao seu repositório GitHub.
3. Adicione as variáveis de ambiente no Render:
    - `API_TOKEN`: Seu token da API.
4. Inicie o deploy.

## Contribuição

1. Fork o repositório.
2. Crie um branch para sua feature (`git checkout -b feature/fooBar`).
3. Commit suas mudanças (`git commit -am 'Add some fooBar'`).
4. Push para o branch (`git push origin feature/fooBar`).
5. Crie um novo Pull Request.

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
Projeto e execução by LEUDO - GWM CarClub

---

Atualize as URLs e outros detalhes conforme necessário.
