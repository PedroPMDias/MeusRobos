import json, os, requests

class Arquivista():
    def __init__(self, cidade, estado):
        self.city = cidade.title()
        self.estate = estado.upper()
        self._biblioteca = str(os.path.dirname(os.path.realpath(__file__))).replace('api_robot', 'biblioteca')
        self.climatempo = str(self._biblioteca + '/climatempo.json')
        
        self.dir_previsoes = str(os.path.dirname(os.path.realpath(__file__))).replace('api_robot', 'previsoes')

    def ler_json(self):
        dados = json.load(open(self.climatempo, 'r'))
        try:
            grupo = dados[self.estate][self.city]
        except Exception:
            print('buscar na internet')
            return False
        else:
            print('buscar no servidor')
            return grupo
    
    def escrever_json(self, up_data):
        new_est, new_cid = list(up_data.keys())[0], list(up_data.values())[0]
        old_data = json.load(open(self.climatempo, 'r'))
        old_cid = old_data[new_est]
        old_cid.update(new_cid)
        old_data[new_est] = old_cid
        with open(self.climatempo, 'w') as ct_json:
            return json.dump(old_data, ct_json, indent=4)

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
