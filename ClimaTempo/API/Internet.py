import requests
from bs4 import BeautifulSoup as bs4

class Frontend():
    def __init__(self, lugar):
        self.chavedojson = str(lugar.replace(' ', '').replace('/', '_')).title()
        self.sufixo = self.chavedojson.replace('_', '-').lower()
        self.google = str(f"https://www.google.com/search?q=previsao+climatempo+{self.sufixo}").replace(' ', '+')
        self.radicais = ('/agora', '', '/amanha', '/fim-de-semana', '/15-dias')

    def _pesquisar_urls(self):
        html = requests.get(self.google)
        if (html.status_code == 200) and (html.ok == True):
            pagina = bs4(html.content, 'lxml')
            tags = pagina.find_all('a')
        
        href = list(map(lambda tag: tag.attrs.get('href'), tags))
        href_bruto = list(filter(lambda bruto: bruto.startswith('/url'), href))
        href_limpo = list(map(lambda limpo: limpo.split('=')[1][:-3], href_bruto))
        urls = list(filter(lambda fixo: fixo.endswith(self.sufixo), href_limpo))
        urls.sort()

        return urls
    
    def _titulacao(self, lista_links):
        titulos = {self.chavedoJson: {}}
        for link in lista_links:
            pagina = requests.get(link)
            if (pagina.status_code == 200) and (pagina.ok == True):
                html = bs4(pagina.content, 'lxml')
                titulos[str(html.title.text)] = link
        return titulos
    
    def pegarUrls(self):
        lista_urls = self._pesquisar_urls()
        urlFatiada = lista_urls[-1].split('/')
        
        for radical in self.radicais:
            url_X = str(f"{urlFatiada[0]}//{urlFatiada[2]}/{urlFatiada[3]}{radical}/{urlFatiada[-3]}/{urlFatiada[-2]}/{urlFatiada[-1]}")
            if url_X not in lista_urls:
                lista_urls.append(url_X)
        urls = list(set(lista_urls))

        return self._titulacao(urls)

"""
front = Frontend('Rio de Janeiro/RJ')
print(front.pegarUrls())
"""