# Importação das bibliotecas
from API.Servidor import Backend
from API.Internet import Frontend

# Cidade da busca
lugar = "Rio de Janeiro/RJ"

# Instaciando as classes
back = Backend()
front = Frontend(lugar)

# Iniciando o processador
if __name__ == "__main__":
    #lista_urls = back.climatizar(lugar)
    #print(lista_urls)
    lista_urls = front.completar_urls()
    print(lista_urls)
    