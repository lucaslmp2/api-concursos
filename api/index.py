import requests
from bs4 import BeautifulSoup

URL = "https://concursosnobrasil.com/concursos-abertos/"  # ou o link correspondente

def get_concursos_abertos():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    concursos = []

    # Seleciona a tabela da aba "Nacional"
    nacional_div = soup.find('div', id='nacional')
    tabela = nacional_div.find('table')
    linhas = tabela.find_all('tr')

    for linha in linhas:
        colunas = linha.find_all('td')
        if len(colunas) == 2:
            link_tag = colunas[0].find('a')
            nome = link_tag.text.strip()
            link = link_tag['href']
            vagas = colunas[1].text.strip()

            concursos.append({
                'organization': nome,
                'link': link,
                'workPlacesAvailable': vagas,
                'status': 'open'  # aqui você pode adaptar se quiser detectar "esperado"
            })
    
    return concursos

# Exemplo de uso
if __name__ == "__main__":
    for concurso in get_concursos_abertos():
        print(concurso)
