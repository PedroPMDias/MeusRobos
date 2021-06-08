import json, os

class Backend():
    def __init__(self, lugar):
        self.chavedoJson = str(lugar.replace(' ', '').replace('/', '_')).upper()
        self.pasta = str(os.path.dirname(os.path.realpath(__file__)))
        self.dir_Previsoes = self.pasta.replace('API', 'Previsoes')
        self.dir_Registros = self.pasta.replace('API', 'Registros')
        self.historico = self.dir_Registros + '/historico.json'

    def _titulacao(self, thisJson):
        jsonValues = dict(thisJson)
        
        for title, url in jsonValues.items(): ### RuntimeError: dictionary keys changed during iteration
            jsonValues[str(f"{self.dir_Previsoes}/{title}")] = url
            jsonValues.pop(title)
            
        return thisJson

    def renovarUrls(self, jsonLocal):
        novoJson = self._titulacao(jsonLocal)
        with open(self.historico, 'w', encoding='utf-8') as arquivo:
            json.dump(novoJson, arquivo, indent=4, ensure_ascii=False)
        return novoJson

    def pegarUrls(self):
        with open(self.historico, 'r') as arquivo:
            leitura = json.load(arquivo)
            try:
                urls = leitura[self.chavedoJson]
            except Exception as erro:
                print(f"Não achei o local -> {erro}. Mas vou baixar e renovar o conteudo todo")
                return False
            else:
                print('Server found local ->', self.chavedoJson)
                return urls

    def prever_arquivos(self, arquivos):
        if not os.path.exists(self.dir_Previsoes):
            dir_local = self.dir_Previsoes + '/' + self.chavedoJson
            os.mkdir(self.dir_Previsoes)
            os.mkdir(dir_local)

        chaves = arquivos.values()
        for chave in chaves.keys():
            if not os.path.exists(chave):
                print(chave)

'''
back = Backend("Rio de Janeiro/RJ")
dict_urls = back.pegarUrls()
urls_renovadas = back.renovarUrls(dict_urls)
print(back.prever_arquivos(urls_renovadas))
'''