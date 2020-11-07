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

    def Recuperar(self,a,AnalisadorLexico,pilha,tokenSeguinte):
        s = pilha[-1]
        for item in self.ACTION[s]:
            if self.ACTION[s][item][0] == 's':
                t = int(self.ACTION[s][a.token][1:])
                pilha.append(t)
                #print('SHIFT')
            elif self.ACTION[s][item][0] == 'r':
                regra = int(self.ACTION[s][a.token][1:])
                A,Beta = Gramatica[regra]
                for cont in range(0,len(Beta)):
                    if len(pilha) <= 0:
                        break
                    pilha.pop()
                t = pilha[-1]
                pilha.append(int(GOTO[t][A]))
                
        """while not(a.lexema in self.Delimitador):
            a = main.getToken(AnalisadorLexico)
        while pd.isnull(self.ACTION[pilha[-1]][a.token]):
            a = main.getToken(AnalisadorLexico)
            pilha.pop()"""
        
        return a,AnalisadorLexico,pilha