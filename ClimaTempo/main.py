# Importação das bibliotecas
from API.Servidor import Backend
from API.Internet import Frontend

# Cidade da busca
lugar = "Rio de Janeiro/RJ" #lugar = "Rio das Ostras/RJ"

# Instaciando as classes
back = Backend(lugar)
front = Frontend(lugar)

# Iniciando o processador
dict_urls = back.pegarUrls()
if not dict_urls: dict_urls = front.pegarUrls()

urls_renovadas = back.renovarUrls(dict_urls) # Inspecionar esse cara aqui
print(back.prever_arquivos(urls_renovadas))

'''
Monte o html geral com todos os fragmentos
'''
