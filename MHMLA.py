import os
from datetime import datetime, timedelta
import pandas as pd
import shutil
import sys
import re

DIRETORIO_ATUAL = 'pasta aonde o robo vai rodar'
DIRETORIO_RAIZ = '\\'.join(DIRETORIO_ATUAL.split('\\')[:5])
CAMINHO_OUTPUT = 'caminho aonde irá salvar o relatório'
CAMINHO_INPUT = 'caminho aonde irá pegar os arquivos de cada dev'

if not DIRETORIO_RAIZ in sys.path:
    sys.path.append(DIRETORIO_RAIZ)

DICT_CONVERSAO_MES_INTEIRO = {
'01': 'Janeiro', '02': 'Fevereiro', '03': 'Março',
'04': 'Abril',   '05': 'Maio',      '06': 'Junho',
'07': 'Julho',   '08': 'Agosto',    '09': 'Setembro', 
'10': 'Outubro', '11': 'Novembro',  '12': 'Dezembro'}

def main():

    DATA_ATUAL = datetime.now()

    nomeDevs = receber_nome_devs(DATA_ATUAL)

    relatorio = open('relatorio-'+DATA_ATUAL.strftime('%d-%m-%Y')+'.txt', 'a+')
    relatorio.write('Feitos ('+DATA_ATUAL.strftime('%d/%m/%Y')+'):\n')
    tarefas_feitas = []
    metas_hoje = []
    cancelarOperacao = False

    for dev in nomeDevs:

        nomeArquivo = 'daily_'+dev+'_'+DATA_ATUAL.strftime('%d')+'_'+DATA_ATUAL.strftime('%m')+'_'+DATA_ATUAL.strftime('%Y')+'.txt'
        arquivo = ler_arquivo(nomeArquivo)

        if 'O que foi feito anteriormente' not in arquivo or 'Metas de hoje:' not in arquivo:
            cancelarOperacao = True
            continue

        nomePessoa = arquivo[0]
        tarefas_anteriores, tarefas_atuais = extrair_tarefas(arquivo)

        tarefas_feitas.append(nomePessoa + ':')
        tarefas_feitas.extend(tarefas_anteriores + [''])
        metas_hoje.append(nomePessoa + ':')
        metas_hoje.extend(tarefas_atuais + [''])

    if not cancelarOperacao:

        for dev in nomeDevs:
            nomeArquivo = 'daily_'+dev+'_'+DATA_ATUAL.strftime('%d')+'_'+DATA_ATUAL.strftime('%m')+'_'+DATA_ATUAL.strftime('%Y')+'.txt'

            diretorioDev = CAMINHO_OUTPUT + dev.capitalize() + '\\' + DATA_ATUAL.strftime('%Y') + '\\' + DICT_CONVERSAO_MES_INTEIRO[DATA_ATUAL.strftime('%m')] + '\\'
            shutil.move(CAMINHO_INPUT + '\\' + nomeArquivo, diretorioDev)

        gerar_relatorio_final(tarefas_feitas, metas_hoje, DATA_ATUAL)
    else:
        cancelarOperacao = 'Cancelada a geração do relatório final.'

def receber_prox_dia_util():

    dfDatasFeriados = pd.read_excel('https://www.anbima.com.br/feriados/arqs/feriados_nacionais.xls', skipfooter=9) 
    dfDatasFeriados['Data'] = pd.to_datetime(dfDatasFeriados['Data'])
    datasFeriados = dfDatasFeriados['Data'].tolist()
    data = datetime.strptime(datetime.now().strftime('%d/%m/%Y') + ' 00:00:00', '%d/%m/%Y %H:%M:%S') + timedelta(1) 
    while data in datasFeriados or data.weekday() > 4:
        data = data + timedelta(1)
    return data

def receber_nome_devs(data_atual):

    arquivosNaPasta = 'vai ler todos os arquivos(txt) dentro da pasta que passar'

    arquivosNomeCorreto = []
    for nomeArquivo in arquivosNaPasta:
        if re.search(f'^daily_[a-zA-Z]{1,}_'+data_atual.strftime('%d')+'_'+data_atual.strftime('%m')+'_'+data_atual.strftime('Y')+'[.]txt', nomeArquivo):
            arquivosNomeCorreto.append(nomeArquivo)
        else:
            nomeArquivo = 'Arquivo com nome incorreto!'
    return [nomeArquivo[6:6 + nomeArquivo[6:].index('_')] for nomeArquivo in arquivosNomeCorreto]

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

def ler_arquivo(nome_arquivo):

    # Abrir o arquivo do dia que o robô vai rodar
    with open(CAMINHO_INPUT + nome_arquivo) as f:
        arquivo = f.read().split('\n') # Lendo o arquivo
    return arquivo

def gerar_relatorio_final(tarefasAnteriores, tarefasAtuais, data_atual):

    diretorioGeral =  CAMINHO_OUTPUT + 'Geral\\' + data_atual.strftime('%Y') + '\\' + DICT_CONVERSAO_MES_INTEIRO[data_atual.strftime('%m')] + '\\'
    relatorio = open(diretorioGeral + 'relatorio-'+data_atual.strftime('%d-%m-%Y')+'_'+data_atual.strftime('%H%M%S')+'.txt', 'a+')

    relatorio.write('Feitos ('+data_atual.strftime('%d/%m/%Y')+'):\n')
    for item in tarefasAnteriores:
        relatorio.write(item + '\n')

    diaUtil = receber_prox_dia_util()
    relatorio.write('A fazer ('+diaUtil.strftime('%d/%m/%Y')+'):\n')
    for item in tarefasAtuais:
        relatorio.write(item + '\n')

    relatorio.close()

if __name__ == '__main__':
    main()