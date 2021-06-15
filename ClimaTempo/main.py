# Importação das bibliotecas
from API.Servidor import Backend
from API.Internet import Frontend

# Cidade da busca ##lugar = "Rio das Ostras/RJ"
lugar = "Rio de Janeiro/RJ"

# Instaciando as classes
back, front = Backend(lugar), Frontend(lugar)

# Buscando no servidor
dict_urls = back.pegar_Urls()

# Buscando na internet e salvando novo json
if not isinstance(dict_urls, dict):
    back.renovarUrls(front.pegar_Urls())
    dict_urls = back.pegar_Urls()

# Verificar a existencia dos arquivos
print(front.download_html(back.existencia_arquivos(dict_urls)))

'''###Montar o html geral com todos os fragmentos'''
