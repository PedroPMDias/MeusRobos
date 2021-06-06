import json, os

class Backend():
    def __init__(self, local):
        self.chavedojson = local.replace('/', '_').replace(' ', '')
        self.pasta = str(os.path.dirname(os.path.realpath(__file__)))
        self.pasta_Registros = self.pasta.replace('API', 'Registros')
        self.historico = self.pasta_Registros + '/historico.json'
        if not os.path.exists(self.pasta_Registros):
            os.mkdir(self.pasta_Registros)
        self.pasta_Previsoes = self.pasta.replace('API', 'Previsoes')
        if not os.path.exists(self.pasta_Previsoes):
            os.mkdir(self.pasta_Previsoes)

    def lerJson(self):
        with open(self.historico, 'r') as jf:
            return json.load(jf)
    
    def escreverJson(self, novoJson):
        with open(self.historico, 'w') as jf:
            return json.dump(novoJson, jf, indent=4)

    def montarNovoJson(self, lista):
        return {self.chavedojson: lista}

    def trazer_urls(self):
        leitura = self.lerJson()

        try:
            urls = leitura[self.chavedojson]
        except KeyError as ke:
            print(f"Não achei o local -> {ke}")
            return False
        else:
            return urls

"""
back = Backend("Rio de Janeiro/RJ")
print(back.trazer_urls())
"""