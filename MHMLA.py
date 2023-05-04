import os
from datetime import datetime, timedelta
import pandas as pd
import sys

DIRETORIO_ATUAL = os.getcwd()[0].upper() + os.getcwd()[1:]
DIRETORIO_RAIZ = '\\'.join(DIRETORIO_ATUAL.split('\\')[:5])

if not DIRETORIO_RAIZ in sys.path:
    sys.path.append(DIRETORIO_RAIZ)

def receberProxDiaUtil(): 
    dfDatasFeriados = pd.read_excel('https://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls', skipfooter=9) 
    dfDatasFeriados['Data'] = pd.to_datetime(dfDatasFeriados['Data'])
    datasFeriados = dfDatasFeriados['Data'].tolist()
    data = datetime.strptime(datetime.now().strftime('%d/%m/%Y') + ' 00:00:00', '%d/%m/%Y %H:%M:%S') + timedelta(1) 
    while data in datasFeriados or data.weekday() > 4:
        data = data + timedelta(1)
    return data

def main():
    DIA_UTIL = receberProxDiaUtil()
    DATA_ATUAL = datetime.now()

    nomeDevs = ['Henrique', 'Marlon']

    relatorio = open('relatorio-'+DATA_ATUAL.strftime('%d-%m-%Y')+'.txt', 'a+')
    relatorio.write('Feitos ('+DATA_ATUAL.strftime('%d/%m/%Y')+'):\n')
    tarefas_feitas = []
    metas_hoje = []

    for dev in nomeDevs:
        arquivo = ler_arquivo(DATA_ATUAL, dev)
        tarefas_anteriores, tarefas_atuais = extrair_tarefas(arquivo)
        nomePessoa = arquivo[0]
        tarefas_feitas.append(nomePessoa + ':')
        tarefas_feitas.extend(tarefas_anteriores + [''])
        metas_hoje.append(nomePessoa + ':')
        metas_hoje.extend(tarefas_atuais + [''])
    gerar_relatorio_final(tarefas_feitas, metas_hoje, relatorio)
    relatorio.close()

def extrair_tarefas(arquivo):
    feitoOntem = arquivo[arquivo.index('O que foi feito anteriormente:')+1:arquivo.index('Metas de hoje:')]
    metasHoje = arquivo[arquivo.index('Metas de hoje:')+1:]
    tarefasAnteriores = []
    tarefasAtuais = []

    for item in feitoOntem:
        if item != '':
            tarefasAnteriores.append(item)

    for item in metasHoje:
        if item != '':
            tarefasAtuais.append(item)
    return (tarefasAnteriores, tarefasAtuais)
    

def ler_arquivo(data_atual, nome_pessoa):

    # Abrir o arquivo do dia que o robô vai rodar
    with open('daily_'+nome_pessoa+'_'+data_atual.strftime('%d')+'_'+data_atual.strftime('%m')+'_'+data_atual.strftime('%Y')+'.txt', 'r') as f:
        arquivo = f.read().split('\n') # Lendo o arquivo
    return arquivo


def gerar_relatorio_final(tarefasAnteriores, tarefasAtuais, relatorio):
    diaUtil = receberProxDiaUtil()

    for item in tarefasAnteriores:
        relatorio.write(item + '\n')

    relatorio.write('A fazer ('+diaUtil.strftime('%d/%m/%Y')+'):\n')
    for item in tarefasAtuais:
        relatorio.write(item + '\n')

main()