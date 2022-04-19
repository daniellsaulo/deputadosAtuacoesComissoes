#processamento dos dados do ano escolhido pra extrair os dados dos
#deputados, como ID, Nome e CPF, armazenando-os no arquivo arquivo dadosDeputados.csv

import pandas as pd

def baixarDadosDeputados(ano, formato):
  print('Baixando os dados dos deputados...')
  df = pd.read_csv('http://www.camara.leg.br/cotas/Ano-{}.{}.zip'.format(ano, formato), encoding='utf-8', sep=';')

  #eliminando dados nulos
  df_clean = df.dropna(subset=['ideCadastro'], axis=0)

  #inserindo numa lista os ID's dos deputados
  idDeputados = df_clean.ideCadastro.unique()
  idDeputados = list(map(int, idDeputados))

  df_clean.set_index('ideCadastro', inplace=True)

  dfDeputados = pd.DataFrame(columns=['id', 'idDeputado', 'Nome', 'cpf'])
  dfDeputados.set_index('id', inplace=True)

  dfDeputados.loc[0] = [idDeputados[0],df_clean.loc[62881,'txNomeParlamentar'],'cpf']

  #preenchendo DF
  for id in range(len(idDeputados)):
    nome = pd.Series(df_clean.loc[idDeputados[id],'txNomeParlamentar'])
    nome = nome.drop_duplicates().values.tolist()
    cpf = pd.Series(df_clean.loc[idDeputados[id],'cpf'])
    cpf = cpf.drop_duplicates().values.tolist()
    cpf = list(map(int, cpf))
    cpf = list(map(str, cpf))

    dfDeputados.loc[id] = [idDeputados[id], nome[0], cpf[0]]

  dfDeputados.to_csv('dadosDeputados.csv')

  print('Download dos dados dos deputados realizado com sucesso!')
