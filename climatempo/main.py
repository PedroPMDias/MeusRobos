from api_robot.arquivos import Arquivista
from api_robot.internet import Navegador
import os
#from api_robot.modelador import something

local_c, local_e = "rio de janeiro", "rj"

interno = Arquivista(cidade=local_c, estado=local_e)
externo = Navegador(cidade=local_c, estado=local_e)

def escrever_previsoes(servidor=interno, internet=externo):
    urls = servidor.get_urls()
    pasta = str(f"{servidor.dir_previsoes}/{servidor.city.replace(' ', '')}_{servidor.estate}/")
    if not os.path.exists(pasta):
        os.mkdir(pasta)
    if urls == False:
        urls = internet.get_urls()
        servidor.set_urls(urls)
    else:
        for nome, url in urls.items():
            url_file = pasta + nome
            if not os.path.exists(url_file):
                print(internet.download(url, url_file))
            else:
                print(url_file)

escrever_previsoes()