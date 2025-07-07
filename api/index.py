import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)
URL = "https://concursosnobrasil.com/concursos-abertos/"


def get_concursos_abertos():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    concursos = []
    nacional_div = soup.find('div', id='nacional')
    if not nacional_div:
        return []

    tabela = nacional_div.find('table')
    if not tabela:
        return []

    linhas = tabela.find_all('tr')
    for linha in linhas:
        colunas = linha.find_all('td')
        if len(colunas) == 2:
            link_tag = colunas[0].find('a')
            if not link_tag:
                continue

            nome = link_tag.text.strip()
            link = link_tag['href']
            vagas = colunas[1].text.strip()

            concursos.append({
                'organization': nome,
                'link': link,
                'workPlacesAvailable': vagas,
                'status': 'open'
            })
    
    return concursos


@app.route('/')
def home():
    return '👋 API de Concursos está online!'

@app.route('/concursos/nacional', methods=['GET'])
def concursos_nacional():
    concursos = get_concursos_abertos()
    return jsonify(concursos)

# NÃO use app.run() — a Vercel vai invocar automaticamente o app
