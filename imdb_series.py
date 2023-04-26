# -*- coding: utf-8 -*-
"""IMDB_Series.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dflz_DFA5ly5nKA_fEiXZmeHTX-zRkVt
"""

#Bibliotecas que serão utilizadas
import requests
import csv
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup

pagina_html = requests.get('https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250').text
pagina = BeautifulSoup(pagina_html, 'html.parser')

#tratando_pagina = pagina.prettify()
#print(tratando_pagina)

tabela = pagina.find(class_='lister-list')
#print(tabela)

conteudo_extraido = []

for linha in tabela.find_all('tr'):
  textos_coluna = list()
  for coluna in linha.find_all('td'):
    texto_coluna = coluna.get_text().strip().split('\n')
    textos_coluna += texto_coluna
    conteudo_extraido.append(texto_coluna)

#print(conteudo_extraido)
#print(len(conteudo_extraido))

#Remoção das informações indesejadas

for i in conteudo_extraido:
  if ['12345678910 ', '', '', '', 'NOT YET RELEASED', ' ', '', 'Seen'] in conteudo_extraido:
    conteudo_extraido.remove(['12345678910 ', '', '', '', 'NOT YET RELEASED', ' ', '', 'Seen'])
  else:
    pass

#print(conteudo_extraido)
#print(len(conteudo_extraido))

for i in conteudo_extraido:
  if [''] in conteudo_extraido:
    conteudo_extraido.remove([''])
  else:
    pass

#print(conteudo_extraido)
#print(len(conteudo_extraido))

#print(str(conteudo_extraido[0]))
#print(str(conteudo_extraido[1]))

ranking = [int(i[0].strip('.')) for i in conteudo_extraido if isinstance(i[0], str) and i[0].strip('.').isdigit()]
nome_serie = [i[1].strip() for i in conteudo_extraido if len(i) > 1 and isinstance(i[1], str)]
ano_serie = [int(i[2].strip('()')) for i in conteudo_extraido if len(i) > 2 and isinstance(i[2], str)]
avaliacao_serie = [float(i[0]) for i in conteudo_extraido if isinstance(i[0], str) and not i[0].strip('.').isdigit()]

#print(ranking)
#print(nome_serie)
#print(ano_serie)
#print(avaliacao_serie)

#Vamos agora, transportar as informações para um arquivo CSV: Lista_Completa.csv

with open(file='Lista_Completa.csv', mode='w', encoding='utf8') as arquivo:
  escritor_csv = csv.writer(arquivo, delimiter=';')

  for i in range(0, len(ranking)):
    rank = str(ranking).replace('[', '').replace(']', '').split(sep=',')
    name = str(nome_serie).replace("'", '').replace('[', '').replace(']', '').replace('"', '').split(sep=',')
    ano = str(ano_serie).replace("'", '').replace('[', '').replace(']', '').split(sep=',')
    avaliacao = str(avaliacao_serie).replace("'", '').replace('[', '').replace(']', '').split(sep=',')

    escritor_csv.writerow([rank[i], name[i], ano[i], avaliacao[i]])
    i = i+1
  
  arquivo.close()