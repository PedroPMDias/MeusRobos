from api_robot.arquivos import Arquivista
from api_robot.internet import Navegador
#from api_robot import modelador

city = 'sao jose dos pinhais'
estate = 'pr'

def controller(cidade, estado):
    arquivo = Arquivista(cidade, estado)
    try:
        grupo = arquivo.ler_json()
    except:
        return False
    else:
        if isinstance(grupo, bool):
            nav = Navegador(cidade, estado)
            grupo = nav.raspar_google()
            arquivo.escrever_json(grupo)
            return arquivo.reagrupar(grupo)
        elif isinstance(grupo, dict):
            return arquivo.reagrupar(grupo)

ctrl = controller(city, estate)

print(ctrl)
