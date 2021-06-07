import json, os

class Backend():
    def __init__(self, lugar):
        self.chavedojson = str(lugar.replace(' ', '').replace('/', '_')).title()
        self.pasta = str(os.path.dirname(os.path.realpath(__file__)))
        self.dir_Previsoes = self.pasta.replace('API', 'Previsoes')
        self.dir_Registros = self.pasta.replace('API', 'Registros')
        self.historico = self.dir_Registros + '/historico.json'

    def _titulacao(self, novoJson):
        urlsNovas = novoJson.values()
        for title, url in urlsNovas:
            urlsNovas[str(f"{self.dir_Previsoes}/{title}")] = url
            urlsNovas.pop(title)
        return novoJson

    def renovarUrls(self, novoLocal):
        novoJson = self._titulacao(novoLocal)
        with open(self.historico, 'w', encoding='utf-8') as arquivo:
            json.dump(novoJson, arquivo, indent=4, ensure_ascii=False)
        return novoJson

    def pegarUrls(self):
        with open(self.historico, 'r') as arquivo:
            leitura = json.load(arquivo)
            try:
                urls = leitura[self.chavedojson]
            except KeyError as ke:
                print(f"Não achei o local -> {ke}. Mas vou baixar e renovar o conteudo todo")
                return False
            else:
                print('Server found local ->', self.chavedojson)
                return urls

    def prever_arquivos(self, arquivos):
        dir_local = self.dir_Previsoes + '/' + self.chavedojson
        if not os.path.exists(self.dir_Previsoes):
            os.mkdir(self.dir_Previsoes) and os.mkdir(dir_local)

        chaves = arquivos.values()
        for chave in chaves.keys():
            if not os.path.exists(chave):
                print(chave)
"""
back = Backend("Rio de Janeiro/RJ")
print(back.pegarUrls())
"""