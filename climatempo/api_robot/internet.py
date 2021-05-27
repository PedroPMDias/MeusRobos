import requests
from bs4 import BeautifulSoup

class Navegador():
    def __init__(self, cidade, estado):
        self.cid = cidade.title().replace(' ', '+')
        self.est = estado.upper()
        self.sufixo = str(f"{self.cid}-{self.est}").lower()
        self.url_google = str(f"https://www.google.com/search?q='previsao+climatempo'+{self.sufixo}")
    
    def agrupador(self, grupo):
        previsoes = {self.est: {self.cid: {}}}
        for link in grupo:
            fatia = link.split('/')[4].replace('-', ' ')
            if fatia == 'cidade':
                name = str(f"Previsao do tempo hoje em {self.cid} - {self.est} _ Climatempo.html")
            else:
                name = str(f"Previsao do tempo {fatia} em {self.cid} - {self.est} _ Climatempo.html")
            previsoes[self.est][self.cid][name] = link
        return previsoes

    def limpeza(self, lista_urls):
        if len(lista_urls) != 5:
            raspas = lista_urls[0].split('/')
            for radical in ('/agora/', '/', '/amanha/', '/fim-de-semana/', '/15-dias/'):
                rdcl = str(f"{raspas[0]}//{raspas[2]}/{raspas[3]}" + radical + f"{raspas[-3]}/{raspas[-2]}/{raspas[-1]}")
                if rdcl not in lista_urls:
                    lista_urls.append(rdcl)
            return self.agrupador(lista_urls)
        else:
            return self.agrupador(lista_urls)
    
    def filtrar_tags(self, tags_a):
        href_bruto = list(map(lambda bruto: str(bruto.get('href')), tags_a))
        href_limpo = list(map(lambda limpo: limpo.split('=')[1][:-3] if limpo.startswith('/url') else '', href_bruto))
        hrefs = []
        for limpo in href_limpo:
            if limpo.endswith(self.sufixo) and ('/vento/' not in limpo) and ('/climatologia/' not in limpo):
                hrefs.append(limpo)
        return self.limpeza(hrefs)

    def raspar_google(self):
        pagina = requests.get(self.url_google)
        filtro = BeautifulSoup(pagina.text, 'lxml')
        main = filtro.find('div', {'id': 'main'})
        tags = list(main.findAll('a'))
        return self.filtrar_tags(tags)
