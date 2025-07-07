from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# ✅ Habilita CORS para qualquer origem (ideal para dev local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique ["http://127.0.0.1:5500"] no lugar do "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scraping")
def pegar_concursos():
    url = "https://URL-DO-SITE-REAL.com"  # Lembre de trocar pelo link real
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    concursos = []

    for item in soup.select('.q-contest-item'):
        titulo = item.select_one('.q-type + .q-title')
        data = item.select_one('.q-item:nth-child(1) .q-title')
        salario = item.select_one('.q-icon-dollar-sign + .q-title')
        link = item.select_one('a')

        concursos.append({
            'titulo': titulo.text.strip() if titulo else '',
            'data': data.text.strip() if data else '',
            'salario': salario.text.strip() if salario else '',
            'link': link['href'] if link else ''
        })

    return { "concursos": concursos }
