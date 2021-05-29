import json
import os
import requests

class Arquivista():
    def __init__(self, cidade, estado):
        self.city = cidade.title()
        self.estate = estado.upper()
        self._biblioteca = str(os.path.dirname(os.path.realpath(__file__))).replace('api_robot', 'biblioteca')
        self.climatempo = self._biblioteca + '/climatempo.json'
        self.dir_previsoes = self.climatempo.replace('api_robot', 'previsoes')

    def get_urls(self):
        urls = json.load(open(self.climatempo, 'r'))
        try:
            grupo = urls[self.estate][self.city]
        except:
            return False
        else:
            return grupo

    def update_urls(self, new_urls):
        old_urls = json.load(open(self.climatempo, 'r'))
        old_city = old_urls[self.estate]
        new_city = new_urls[self.estate]
        old_city.update(new_city)
        old_urls[self.estate] = old_city
        return old_urls

    def set_urls(self, up_urls):
        up_data = self.update_urls(up_urls)
        return json.dump(up_data, open(self.climatempo, 'w'), indent=4)

    '''
    def criar_previsao(self, arquivo, url):
        pagina = requests.get(url)
        try:
            previsao = open(arquivo, 'w')
            previsao.write(str(pagina.text))
        except Exception as criacao:
            return criacao
        else:
            previsao.close()

    def reagrupar(self, previsoes):
        for estado, cidades in previsoes.items():
            for cidade, conjunto in cidades.items():
                for nome, link in conjunto.items():
                    html = str(self.dir_previsoes + f"/{cidade}_{estado}")
                    if not os.path.exists(html):
                        os.mkdir(html)
                    html_file = str(f"{html}/{nome}")
                    print(self.criar_previsao(html_file, link))
    '''
