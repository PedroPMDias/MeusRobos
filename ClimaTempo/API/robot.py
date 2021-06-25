import requests, random, json, os
from bs4 import BeautifulSoup as bs4

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
                pagina = bs4(pedido.content, 'lxml')
        except Exception:
            return False
        else:
            return pagina
    
    def _filtrar_urls(self, pagina):
        tags = pagina.find_all('a')
        href = list(map(lambda tag: tag.attrs.get('href'), tags))
        href_bruto = list(filter(lambda bruto: bruto.startswith('/url'), href))
        href_limpo = list(map(lambda limpo: limpo.split('=')[1][:-3], href_bruto))
        urls = list(filter(lambda fixo: fixo.endswith(self.sufixo), href_limpo))
        return list(set(urls))
    
    def _dar_nome_aos_bois(self, lista_links):
        grupo_urls = {}
        for link in lista_links:
            pedido = self._baixar_pagina(link)
            tag_title = str(pedido.title.text + '.html')
            if not ("Climatologia" in tag_title or "Vento" in tag_title):
                grupo_urls[tag_title] = link
        return grupo_urls
    
    def requisitor(self):
        lista_urls = self._filtrar_urls(self._baixar_pagina(self.google))
        urlFatiada = random.choice(lista_urls).split('/')
        for radical in self.radicais:
            this_link = str(f"{urlFatiada[0]}//{urlFatiada[2]}/{urlFatiada[3]}{radical}/{urlFatiada[-3]}/{urlFatiada[-2]}/{urlFatiada[-1]}")
            if not (this_link in lista_urls):
                lista_urls.append(this_link)
        return self._dar_nome_aos_bois(lista_urls)

    def download_html(self, pedidos):
        if len(pedidos) < 5:
            for nome, link in pedidos.items():
                with open(nome, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(str(self._baixar_pagina(link)))
                    print('\nSucess Download ->', nome)
        else:
            return 'Todos os arquivos já foram baixados'

class Backend(Frontend):
    def __init__(self, lugar):
        self.chavedoJson = str(lugar.replace(' ', '').replace('/', '_')).lower()
        self.pastaAPI = str(os.path.dirname(os.path.realpath(__file__)))
        self.dir_Previsoes = self.pastaAPI.replace('API', 'Previsoes')
        self.historico = str(f"{self.pastaAPI}/historico.json".replace('API', 'Dados'))
        self.dir_Downloads = self.dir_Previsoes + '/' + self.chavedoJson + '/'
        Frontend.__init__(self, lugar)

    def requisitor(self):
        with open(self.historico, 'r', encoding='utf-8') as arquivo:
            try:
                leitura = json.load(arquivo)
                chaves = leitura[self.chavedoJson]
            except KeyError as key:
                print(key, "nao esta no Json.")
                return False
            else:
                return chaves

    def renovarUrls(self, localJson, stepJson={}):
        with open(self.historico, 'w', encoding='utf-8') as local:
            if not os.path.exists(self.dir_Downloads):
                os.makedirs(self.dir_Downloads, exist_ok=True)
            for web_name, url_city in localJson.items():
                stepJson[self.dir_Downloads + web_name] = url_city
            return json.dump({self.chavedoJson: stepJson}, local, indent=4, ensure_ascii=False)

    def existencia_arquivos(self, arquivos, stepJson={}):
        for chave, valor in arquivos.items():
            if os.path.exists(chave):
                stepJson[chave] = valor
        return stepJson

