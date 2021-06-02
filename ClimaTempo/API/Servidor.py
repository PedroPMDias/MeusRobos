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
        pasta_estado = self.pasta_Downloads + f"/{self.estado}"
        pasta_cidade = pasta_estado + f"/{self.cidade}"
        if not os.path.exists(self.pasta_Downloads):
            os.mkdir(self.pasta_Downloads)
        if not os.path.exists(pasta_estado):
            os.mkdir(pasta_estado)
        if not os.path.exists(pasta_cidade):
            os.mkdir(pasta_cidade)

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
    
    def download(self, links):
        for estado, est_key in links.items():
            for cidade, cid_key in est_key.items():
                for nome, url in cid_key.items():
                    endereco = str(f"{self.pasta_Downloads}/{estado}/{cidade}/{nome}")
                    if not os.path.exists(endereco):
                        print(web.download(url, endereco))
                    else:
                        print(endereco)
