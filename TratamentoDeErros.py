import pandas as pd
import main

class Erro:
    def __init__(self,ACTION,Delimitador):
        self.ACTION = ACTION
        self.Delimitador = Delimitador
        self.TabelaDeErros = pd.read_csv("MENSAGEM_ERROS.csv",sep=';',index_col='CodErro')
        self.TabelaDeErros = pd.DataFrame.to_dict(self.TabelaDeErros,orient='index')

    def Apresentar(self,linha,coluna,estado,token):
        if token == 'ERRO':
            print('ERRO LEXICO: Token Invalido na linha '+ str(linha) + ' coluna ' + str(coluna))
            return
        mensagem = 'ERRO SINTATICO:'
        erro = int(self.ACTION[estado][token][1:])
        for item in self.TabelaDeErros[erro]:
             if not pd.isnull(self.TabelaDeErros[erro][item]):
                mensagem = mensagem + '{'+ self.TabelaDeErros[erro][item] + '}'
        mensagem = mensagem + ' esperado antes de linha ' + str(linha) + ' coluna ' + str(coluna)
        print(mensagem)

    def Recuperar(self,a,AnalisadorLexico,pilha):
        while not(a.lexema in self.Delimitador):
            a = main.getToken(AnalisadorLexico)
        while pd.isnull(self.ACTION[pilha[-1]][a.token]):
            a = main.getToken(AnalisadorLexico)
            pilha.pop()
        
        return a,AnalisadorLexico,pilha