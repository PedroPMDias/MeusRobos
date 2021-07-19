import requests, random, json, os
from bs4 import BeautifulSoup as bs4


class Web():
    def __init__(self, cidade):
        self.lugar = cidade
        self.sufixo = self.lugar.replace('+', '-')
        self.google = str(f"https://www.google.com/search?q=previsao+completa+climatempo+{self.lugar}/")
        self.radicais = ['/agora', '', '/amanha', '/fim-de-semana', '/15-dias']

    def _abrirUrl(self, url):
        pedido = requests.get(url)
        try:
            pagina = bs4(pedido.content, 'lxml')
        except Exception:
            return False
        else:
            return pagina
    
    def _filtrarUrls(self, pagina):
        tags = pagina.find_all('a')
        href = list(map(lambda tag: tag.attrs.get('href'), tags))
        href_bruto = list(filter(lambda bruto: bruto.startswith('/url'), href))
        href_limpo = list(map(lambda limpo: limpo.split('=')[1][:-3], href_bruto))
        urls = list(filter(lambda fixo: fixo.endswith(self.sufixo), href_limpo))
        urls = list(set(urls))
        for url in urls:
            if ('climatologia' in url) or ('vento' in url) or ('uv' in url):
                urls.remove(url)
        return urls
    
    def _agruparUrls(self, lista_links):
        grupo_urls = {}
        for link in lista_links:
            pedido = self._abrirUrl(link)
            tag_title = str(pedido.title.text + '.html')
            grupo_urls[tag_title] = link
        return grupo_urls
    
    def links_Internet(self):
        lista_urls = self._filtrarUrls(self._abrirUrl(self.google))
        urlFatiada = random.choice(lista_urls).split('/')
        for radical in self.radicais:
            this_link = str(f"{urlFatiada[0]}//{urlFatiada[2]}/{urlFatiada[3]}{radical}/{urlFatiada[-3]}/{urlFatiada[-2]}/{urlFatiada[-1]}")
            if not (this_link in lista_urls):
                lista_urls.append(this_link)
        return self._agruparUrls(lista_urls)

class ClimaTempo(Web):
    def __init__(self, lugar):
        self.dir_API = str('ClimaTempo/API/' + (os.path.realpath(__file__)))
        self.backup = str(f"{self.dir_API}/backup.json".replace('API', 'Dados'))
        self.json_id = str(lugar.replace(' ', '_')).upper()
        '''
        self.chaveWeb = str(lugar.replace(' ', '').replace('/', '+')).lower()
        self.dir_Previsoes = self.dir_API.replace('API', 'Previsoes')
        self.dir_Downloads = self.dir_Previsoes + '/' + self.chaveWeb + '/'
        Web.__init__(self, self.chaveWeb)'''

    def existemArquivos(self, arquivos):
        for nome, link in arquivos.items():
            if not os.path.exists(nome):
                print(nome, '\n', link)

    def pegar_json(self):
        try:
            os.path.exists(self.backup)
        except EOFError:
            return "JSON nao existe"
        else:
            with open(self.backup, 'r', encoding='utf-8') as backup:
                dados = json.load(backup)
                return self.existemArquivos(dados.get(self.json_id))


ct = ClimaTempo('Rio de Janeiro/RJ')
print(ct.pegar_json())
    
'''
    def procurarArquivos(self, arquivos):
        for nome, link in arquivos[self.chaveWeb].items():
            if not os.path.exists(nome):
                with open(nome, 'w', encoding='utf-8') as arqPrevisao:
                    pgnPrevisao = self._abrirUrl(link)
                    arq = arqPrevisao.write(pgnPrevisao)
                    print(f"\n{arq} - {nome} salvo com sucesso!")
            print(f"\n{nome} ja esta no servidor")

    def trocarJson(self, localJson, stepJson={}):
        if not os.path.exists(self.dir_Downloads):
            os.makedirs(self.dir_Downloads, exist_ok=True)
        with open(self.backup, 'w', encoding='utf-8') as local:
            for web_name, url_city in localJson.items():
                stepJson[self.dir_Downloads + web_name] = url_city
                novoJson = {self.chaveWeb: stepJson}
            json.dump(novoJson, local, indent=4, ensure_ascii=False)
        return self.procurarArquivos(novoJson)

    def links_Servidor(self):
        with open(self.backup, 'r', encoding='utf-8') as arquivo:
            meuJson = json.load(arquivo)
            try:
                leitura = meuJson[self.chaveWeb]
            except KeyError as key:
                print(key, "nao estava no Json. Vou pegar na internet.")
                webLinks = self.links_Internet()
                return self.trocarJson(webLinks)
            else:
                busca = self.procurarArquivos(leitura)
                return busca
'''


"""
teste = {"RiodeJaneiro-RJ": {
        "Previsão do tempo para amanhã em Rio de Janeiro - RJ | Climatempo.html": "https://www.climatempo.com.br/previsao-do-tempo/amanha/cidade/321/riodejaneiro-rj",
        "Previsão do tempo para o fim de semana em Rio de Janeiro - RJ | Climatempo.html": "https://www.climatempo.com.br/previsao-do-tempo/fim-de-semana/cidade/321/riodejaneiro-rj",
        "Previsão do tempo agora em Rio de Janeiro - RJ | Climatempo.html": "https://www.climatempo.com.br/previsao-do-tempo/agora/cidade/321/riodejaneiro-rj",
        "Previsão do tempo para hoje em Rio de Janeiro - RJ | Climatempo.html": "https://www.climatempo.com.br/previsao-do-tempo/cidade/321/riodejaneiro-rj",
        "Previsão do tempo para os próximos 15 dias em Rio de Janeiro - RJ | Climatempo.html": "https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/321/riodejaneiro-rj"}}
print(teste)
"""
