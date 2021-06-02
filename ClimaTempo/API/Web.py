import requests
from bs4 import BeautifulSoup

class Navegador():
    def __init__(self, cidade, estado):
        self._sufixo = str(cidade + '-' + estado).replace(' ', '')
        self._url_google = str(f"https://www.google.com/search?q=previsao+climatempo+{self._sufixo}/").lower()
        self._cidade = cidade.title()
        self._estado = estado.upper()

    def _agrupar_urls(self, grupo):
        previsoes = {self._estado: {self._cidade: {}}}
        for link_arquivo in grupo:
            fatia = link_arquivo.split('/')[4].replace('-', ' ')
            if fatia == 'cidade':
                nome_arquivo = str(f"Previsao do tempo hoje em {self._cidade} - {self._estado} _ Climatempo.html")
            else:
                nome_arquivo = str(f"Previsao do tempo {fatia} em {self._cidade} - {self._estado} _ Climatempo.html")
            
            previsoes[self._estado][self._cidade][nome_arquivo] = link_arquivo

        return previsoes

    def _complementar_urls(self, lista_urls):
        fatia = lista_urls[0].split('/')
        for rdcl in ('/agora/', '/', '/amanha/', '/fim-de-semana/', '/15-dias/'):
            radical = str(f"{fatia[0]}//{fatia[2]}/{fatia[3]}" + rdcl + f"{fatia[-3]}/{fatia[-2]}/{fatia[-1]}")
            if radical not in lista_urls:
                lista_urls.append(radical)
        return self._agrupar_urls(lista_urls)
    
    def _filtrar_tags(self, href_bruto, hrefs = []):
        href_limpo = list(map(lambda limpo: limpo.split('=')[1][:-3] if limpo.startswith('/url') else '', href_bruto))
        for href in href_limpo:
            if href.endswith(self._sufixo):
                if ('/vento/' not in href) and ('/climatologia/' not in href):
                    hrefs.append(href)
        return self._complementar_urls(list(set(hrefs)))

    def pegar_urls(self):
        try:
            pagina = requests.get(self._url_google)
            html = BeautifulSoup(pagina.text, 'lxml')
        except:
            return None
        else:
            tags_a = html.find('div', {'id': 'main'}).findAll('a')
            href = list(map(lambda bruto: str(bruto.get('href')), tags_a))
            return self._filtrar_tags(href)
    
    def download(self, url_pagina, local_arquivo):
        previsao = str(requests.get(url_pagina).text)
        with open(local_arquivo, 'w') as file_html:
            try:
                file_html.write(previsao)
            except Exception as r:
                return r
            else:
                return file_html.name
