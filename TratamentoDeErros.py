import pandas as pd
import main

class Erro:
    def __init__(self,ACTION,Delimitador):
        self.ACTION = ACTION
        self.Delimitador = Delimitador

    def Apresentar(self,linha,coluna,estado,token):
        if token == 'ERRO':
            print('ERRO LEXICO: Token Invalido na linha '+ str(linha) + ' coluna ' + str(coluna))
            return
        mensagem = 'ERRO SINTATICO: '
        for item in self.ACTION[estado]:
            if not(pd.isnull(self.ACTION[estado][item])):
                mensagem = mensagem + item + '/'
        mensagem = mensagem + ' esperado na linha ' + str(linha) + ' coluna ' + str(coluna)
        print(mensagem)

    def Recuperar(self,a,AnalisadorLexico,pilha):
        while not(a.lexema in self.Delimitador):
            a = main.getToken(AnalisadorLexico)
        while pd.isnull(self.ACTION[pilha[-1]][a.token]):
            a = main.getToken(AnalisadorLexico)
            pilha.pop()
        
        return a,AnalisadorLexico,pilha