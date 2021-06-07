"""
from bs4 import BeautifulSoup as bs4
import os

aqui = str(os.path.realpath(os.path.dirname(__file__)) + '/Pesquisa.html')

with open(aqui, 'r') as f:
    html = bs4(f, 'lxml')

h1 = html.title.text
print(h1)
"""