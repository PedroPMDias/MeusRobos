import requests, random, json, os
from bs4 import BeautifulSoup as bs4

class Web():
    def __init__(self, lugar):
        self.__localizacao = str(lugar.replace(' ', '').replace('/', '_'))
        self.__sufixo = self.__localizacao.replace('_', '-')
        self.__google = str(f"https://www.google.com/search?q=previsao+completa+climatempo+{self.__localizacao}").replace('_', '+')
        self.__radicais = ['/agora', '', '/amanha', '/fim-de-semana', '/15-dias']

    def __abrirUrl(self, url):
        try:
            pedido = requests.get(url)
            if (pedido.status_code == 200) and (pedido.ok == True):
                pagina = bs4(pedido.content, 'lxml')
        except Exception:
            return False
        else:
            return pagina
    
    def __filtrarUrls(self, pagina):
        tags = pagina.find_all('a')
        href = list(map(lambda tag: tag.attrs.get('href'), tags))
        href_bruto = list(filter(lambda bruto: bruto.startswith('/url'), href))
        href_limpo = list(map(lambda limpo: limpo.split('=')[1][:-3], href_bruto))
        urls = list(filter(lambda fixo: fixo.endswith(self.__sufixo), href_limpo))
        urls = list(set(urls))
        for url in urls:
            if ('climatologia' in url) or ('vento' in url):
                urls.remove(url)
        return urls
    
    def __agruparUrls(self, lista_links):
        grupo_urls = {}
        for link in lista_links:
            pedido = self.__abrirUrl(link)
            tag_title = str(pedido.title.text + '.html')
            grupo_urls[tag_title] = link
        return grupo_urls
    
    def _links_Internet(self):
        lista_urls = self.__filtrarUrls(self.__abrirUrl(self.__google))
        urlFatiada = random.choice(lista_urls).split('/')
        for radical in self.__radicais:
            this_link = str(f"{urlFatiada[0]}//{urlFatiada[2]}/{urlFatiada[3]}{radical}/{urlFatiada[-3]}/{urlFatiada[-2]}/{urlFatiada[-1]}")
            if not (this_link in lista_urls):
                lista_urls.append(this_link)
        return self.__agruparUrls(lista_urls)

class ClimaTempo(Web):
    def __init__(self, lugar):
        self.__localizacao = str(lugar.replace(' ', '').replace('/', '_')).lower()
        self.__pastaAPI = str(os.path.dirname(os.path.realpath(__file__)))
        self.__dir_Previsoes = self.__pastaAPI.replace('API', 'Previsoes')
        self.__historico = str(f"{self.__pastaAPI}/historico.json".replace('API', 'Dados'))
        self.__dir_Downloads = self.__dir_Previsoes + '/' + self.__localizacao + '/'
        Web.__init__(self, self.__localizacao)

    def _trocarJson(self, localJson, stepJson={}):
        if not os.path.exists(self.__dir_Downloads):
            os.makedirs(self.__dir_Downloads, exist_ok=True)
        
        for web_name, url_city in localJson.items():
            stepJson[self.__dir_Downloads + web_name] = url_city
        novoJson = {self.__localizacao: stepJson}

        with open(self.__historico, 'w', encoding='utf-8') as local:
            json.dump(novoJson, local, indent=4, ensure_ascii=False)
        return novoJson

    def links_Servidor(self):
        with open(self.__historico, 'r', encoding='utf-8') as arquivo:
            try:
                leitura = json.load(arquivo)
                chaves = leitura[self.__localizacao]
            except KeyError as key:
                print(key, "nao estava no Json. Vou pegar na internet.")
                return self._trocarJson(self._links_Internet())
            else:
                return chaves
