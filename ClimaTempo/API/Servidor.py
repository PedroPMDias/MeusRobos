import json, os

class Backend():
    def __init__(self, lugar):
        self.chavedoJson = str(lugar.replace(' ', '').replace('/', '_')).lower()
        self.pastaAPI = str(os.path.dirname(os.path.realpath(__file__)))
        self.dir_Previsoes = self.pastaAPI.replace('API', 'Previsoes')
        self.historico = self.pastaAPI.replace('API', 'Registros') + '/historico.json'
        self.dir_Downloads = self.dir_Previsoes + '/' + self.chavedoJson + '/'

    def pegar_Urls(self):
        with open(self.historico, 'r', encoding='utf-8') as arquivo:
            try:
                leitura = json.load(arquivo)[self.chavedoJson]
            except KeyError:
                print(f"{self.chavedoJson} nao existe no Json.")
                return None
            else:
                return leitura

    def renovarUrls(self, localJson, stepJson={}):
        with open(self.historico, 'w', encoding='utf-8') as local:
            if not os.path.exists(self.dir_Downloads):
                os.makedirs(self.dir_Downloads, exist_ok=True)
            for web_name, url_city in localJson.items():
                stepJson[self.dir_Downloads + web_name] = url_city
            return json.dump({self.chavedoJson: stepJson}, local, indent=4, ensure_ascii=False)

    def existencia_arquivos(self, arquivos, stepJson={}):
        for chave, valor in arquivos.items():
            if not os.path.exists(chave):
                stepJson[chave] = valor
        return stepJson
