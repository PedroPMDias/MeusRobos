from api_robot.arquivos import Arquivista
from api_robot.internet import Navegador
from pprint import pprint
#from api_robot.modelador import something

local_c, local_e = "rio das ostras", "rj"

servidor = Arquivista(cidade=local_c, estado=local_e)
internet = Navegador(cidade=local_c, estado=local_e)

urls = servidor.get_urls() or internet.get_urls()

print(servidor.set_urls(urls))
