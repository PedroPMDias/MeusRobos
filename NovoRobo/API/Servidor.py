import json, os

class Backend():
    def __init__(self):
        self.pasta_Registros = str(os.path.dirname(os.path.realpath(__file__))).replace('API', 'Registros')
        self.historico = self.pasta_Registros + '/historico.json'
        #if not os.path.exists(self.pasta_Registros): os.mkdir(self.pasta_Registros)

    def ler_json(self):
        with open(self.historico, 'r') as jf:
            return json.load(jf)
    
    def escrever_json(self, novoJson):
        with open(self.historico, 'w') as jf:
            return json.dump(novoJson, jf, indent=4)

    def climatizar(self, local):
        cidade = local.split('/')[0]
        estado = local.split('/')[-1]
        leitura = self.ler_json()

        try:
            urls = leitura[estado][cidade]
        except KeyError as ke:
            print(f"Não achei o local -> {ke}")
            return False
        else:
            return urls

"""
lugar = "Rio de Janeiro/RJ"
back = Backend()
back.climatizar(lugar)
"""