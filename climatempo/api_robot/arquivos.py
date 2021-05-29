import json
import os

class Arquivista():
    def __init__(self, cidade, estado):
        self.city = cidade.title()
        self.estate = estado.upper()
        self._biblioteca = str(os.path.dirname(os.path.realpath(__file__))).replace('api_robot', 'biblioteca')
        self._climatempo = self._biblioteca + '/climatempo.json'
        self.dir_previsoes = self._biblioteca.replace('biblioteca', 'Previsoes')

    def get_urls(self):
        urls = json.load(open(self._climatempo, 'r'))
        try:
            grupo = urls[self.estate][self.city]
        except:
            return False
        else:
            return grupo

    def update_urls(self, new_urls):
        old_urls = json.load(open(self._climatempo, 'r'))
        old_city = old_urls[self.estate]
        new_city = new_urls[self.estate]
        old_city.update(new_city)
        old_urls[self.estate] = old_city
        return old_urls

    def set_urls(self, up_urls):
        up_data = self.update_urls(up_urls)
        return json.dump(up_data, open(self._climatempo, 'w'), indent=4)

    