from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from parsel import Selector
import pandas as pd
import idDeputados
from selenium.webdriver.chrome.options import Options

# webdriverGoogleChrome, para busca dos dados pelo navegador Google Chrome, em modo oculto
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('chromedriver', options=chrome_options)


# funcoes para limpar dados importados
def cleanPlenario(plenario):
    plenario = plenario.replace(' ', '')
    plenario = plenario.split('d')
    plenario = plenario[0]
    return plenario


def cleanComissoes(comissao):
    comissao = comissao.replace(' ', '')
    comissao = comissao.split('r')
    comissao = comissao[0]
    return comissao


# leitura do DataFrame com os IDs de cada deputado
idDeputados.baixarDadosDeputados(2021, 'csv')
dfIdDeputados = pd.read_csv('dadosDeputados.csv', index_col='id')
id = dfIdDeputados.idDeputado
idList = id.values.tolist()

# criacao do DataFrame que irá receber os dados das atuacoes e comissoes de cada deputado
dfAtuacoesDeputados = pd.DataFrame(columns=['Nome', 'Propostas De Sua Autoria', 'Propostas Relatadas',
                                            'Votações Em Plenário', 'Discursos Em Plenário', 'Presença Em Plenário',
                                            'Ausências Justificadas Plenário', 'Ausências Não Justificadas Plenário',
                                            'Presença Comissões', 'Ausências Justificadas Comissoes',
                                            'Ausências Não Justificadas Comissões', 'Fonte'])

print('Carregando as atuações e comissões de cada um dos {} deputados encontrados...'.format(len(idList)))

# leitura das atuacoes e comissoes de cada deputado e insercao desses dados no DataFrame
for id in range(len(idList)):

    DATA_URL = "https://www.camara.leg.br/deputados/{}?ano=2021".format(idList[id])
    driver.get(DATA_URL)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'atuacao__quantidade')))

    response = Selector(text=driver.page_source)

    nome = response.css('ul.informacoes-deputado li::text').get()

    listaAutorias = response.css('.atuacao__quantidade::text').getall()
    suaAutoria = int(listaAutorias[0])
    relatadas = int(listaAutorias[1])
    plenario = int(listaAutorias[2])
    discursos = int(listaAutorias[3])

    listaComissoes = response.css('dd.list-table__definition-description::text').getall()

    for idComissoes in range(len(listaComissoes)):
        if 'r' in listaComissoes[idComissoes]:
            listaComissoes[idComissoes] = cleanComissoes(listaComissoes[idComissoes])
        if 'd' in listaComissoes[idComissoes]:
            listaComissoes[idComissoes] = cleanPlenario(listaComissoes[idComissoes])

    presencaPlenario = int(listaComissoes[0])
    ausenciasJustificadasPlenario = int(listaComissoes[1])
    ausenciasNaoJustificadasPlenario = int(listaComissoes[2])
    presencaComissoes = int(listaComissoes[3])
    ausenciasJustificadasComissoes = int(listaComissoes[4])
    ausenciasNaoJustificadasComissoes = int(listaComissoes[5])

    dfAtuacoesDeputados.loc[id] = [nome, suaAutoria, relatadas, plenario, discursos, presencaPlenario,
                                   ausenciasJustificadasPlenario, ausenciasNaoJustificadasPlenario,
                                   presencaComissoes, ausenciasJustificadasComissoes,
                                   ausenciasNaoJustificadasComissoes, DATA_URL]
    print("{}/{} - Dados do(a) deputado(a){} carregados com sucesso!".format(id + 1, len(idList), nome))

# exportação do DataFrame com as atuacoes de cada deputado em formato Excel
dfAtuacoesDeputados.to_excel('AtuacoesDeputados.xlsx', index=False, freeze_panes=(1,0))

driver.close()

print("Relatório em formato .xlsx gerado com sucesso!")