import requests, random
from bs4 import BeautifulSoup as BS4

class Frontend():
    def __init__(self, lugar):
        self.chavedoJson = str(lugar.replace(' ', '').replace('/', '_')).lower()
        self.sufixo = self.chavedoJson.replace('_', '-')
        self.google = str(f"https://www.google.com/search?q=previsao+completa+climatempo+{self.sufixo}")
        self.radicais = ('/agora', '', '/amanha', '/fim-de-semana', '/15-dias')

    def _baixar_pagina(self, url):
        try:
            pedido = requests.get(url)
            if (pedido.status_code == 200) and (pedido.ok == True):
                pagina = BS4(pedido.content, 'lxml')
        except Exception:
            return False
        else:
            return pagina
    
    def _filtrar_urls_google(self):
        pagina = self._baixar_pagina(self.google)
        tags = pagina.find_all('a')
        href = list(map(lambda tag: tag.attrs.get('href'), tags))
        href_bruto = list(filter(lambda bruto: bruto.startswith('/url'), href))
        href_limpo = list(map(lambda limpo: limpo.split('=')[1][:-3], href_bruto))
        urls = list(filter(lambda fixo: fixo.endswith(self.sufixo), href_limpo))
        return list(set(urls))
    
    def _dar_nome_aos_bois(self, lista_links, grupo_urls={}):
        for link in lista_links:
            pedido = self._baixar_pagina(link)
            tag_title = str(pedido.title.text + '.html')
            if not ("Climatologia" in tag_title or "Vento" in tag_title):
                grupo_urls[tag_title] = link
        return grupo_urls
    
    def pegar_Urls(self):
        lista_urls = self._filtrar_urls_google()
        urlFatiada = random.choice(lista_urls).split('/')
        for radical in self.radicais:
            this_link = str(f"{urlFatiada[0]}//{urlFatiada[2]}/{urlFatiada[3]}{radical}/{urlFatiada[-3]}/{urlFatiada[-2]}/{urlFatiada[-1]}")
            if not (this_link in lista_urls):
                lista_urls.append(this_link)
        return self._dar_nome_aos_bois(lista_urls)

    def download_html(self, pedidos):
        if len(pedidos) < 1:
            for nome, link in pedidos.items():
                with open(nome, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(str(self._baixar_pagina(link)))
                    print('Sucess Download ->', nome)
        else:
            return 'Todos os arquivos baixados'
