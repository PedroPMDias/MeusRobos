import json
import os

class Arquivista():
    def __init__(self, cidade, estado):
        self.cidade = cidade.title()
        self.estado = estado.upper()
        self._pasta_Localizacao = str(os.path.dirname(os.path.realpath(__file__))).replace('API', 'Localizacao')
        self._json_Agenda = str(self._pasta_Localizacao + '/Agenda.json')
        self.pasta_Downloads = str(self._pasta_Localizacao.replace('Localizacao', 'Downloads'))

    def criar_pastas(self):
        if not os.path.exists(self.pasta_Downloads):
            os.mkdir(self.pasta_Downloads)
        
        pasta_previsoes = self.pasta_Downloads + f"/{self.estado}_{self.cidade}"
        if not os.path.exists(pasta_previsoes):
            os.mkdir(pasta_previsoes)

    def pegar_urls(self):
        with open(self._json_Agenda, 'r') as arquivo:
            try:
                agenda = json.load(arquivo)
            except json.decoder.JSONDecodeError:
                return {}
            else:
                return agenda

    def salvar_urls(self, novas_urls):
        self.criar_pastas()
        urls = self.pegar_urls()
        urls.update(novas_urls)
        with open(self._json_Agenda, 'w') as agenda:
            json.dump(urls, agenda, indent=4)
        return urls
