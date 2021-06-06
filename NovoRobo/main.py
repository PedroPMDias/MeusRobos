# Importação das bibliotecas
from API.Servidor import Backend
from API.Internet import Frontend

# Cidade da busca
lugar = "Rio das Ostras/RJ"

# Instaciando as classes
back = Backend(lugar)
front = Frontend(lugar)

# Iniciando o processador

if __name__ == "__main__":
    lista_urls = back.trazer_urls() # Lista veio do servidor
    if not lista_urls:
        lista_urls = front.trazer_urls() # Lista veio da internet
    
    # Preparar a lista e salvar lista no json
    url_h1 = front.pegar_titulos(lista_urls)
    novoJson = back.montarNovoJson(url_h1)
    back.escreverJson(novoJson)
    