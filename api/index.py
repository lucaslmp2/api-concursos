from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# 🚨 CORS liberado para funcionar com seu front-end local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/scraping")
def pegar_concursos():
    url = "https://www.qconcursos.com/questoes-de-concursos/concursos"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    concursos = []

    for item in soup.select(".q-contest-item.q-contest-item--abertos"):
        titulo_el = item.select_one(".q-type + .q-title")
        link_el = item.select_one("a[href]")
        data_el = item.select_one(".q-item .q-title")
        salario_el = item.select_one(".q-icon-dollar-sign + .q-title")

        concursos.append({
            "texto": titulo_el.text.strip() if titulo_el else "",
            "data": data_el.text.strip() if data_el else "",
            "salario": salario_el.text.strip() if salario_el else "",
            "link": "https://www.qconcursos.com" + link_el["href"] if link_el else ""
        })

    return {"concursos": concursos}
