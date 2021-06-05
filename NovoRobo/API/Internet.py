import requests, os
from bs4 import BeautifulSoup as bs4

class Frontend():
    def __init__(self, lugar):
        self.chave = str(lugar).replace('/', '-').replace(' ', '').lower()
        self.busca = str(f"climatempo {lugar}").replace('/', ' ')
        self.google = str(f"https://www.google.com/search?q={self.busca}").replace(' ', '+')

    def pesquisar_urls(self):
        html = requests.get(self.google)
        if (html.status_code == 200) and (html.ok == True):
            pagina = bs4(html.content, 'lxml')
            tags = pagina.find_all('a')
        
        hrefs = list(map(lambda tag: tag.attrs.get('href'), tags))
        href_bruto = list(filter(lambda bruto: bruto.startswith('/url'), hrefs))
        href_limpo = list(map(lambda limpo: limpo.split('=')[1][:-3], href_bruto))
        urls = list(filter(lambda url: url.endswith(self.chave), href_limpo))

        return urls
    
    def completar_urls(self):
        links = self.pesquisar_urls()
        linkT = links[0].split('/')
        
        for radical in ('/agora', '', '/amanha', '/fim-de-semana', '/15-dias'):
            url = str(f"{linkT[0]}//{linkT[2]}/{linkT[3]}{radical}/{linkT[-3]}/{linkT[-2]}/{linkT[-1]}")
            if url not in links:
                links.append(url)
        
        return links

"""
front = Frontend('Rio de Janeiro/RJ')
clima = front.completar_urls()
print(clima)
"""