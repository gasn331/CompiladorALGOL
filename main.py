from Lexico import Lexico
import pandas as pd
import sys
from TabelaDeSimbolos import TabelaDeSimbolos
"""
Execucao: python main.py [Arquivo de entrada]
"""
Delimitador = [';','fimse','fim',')','$', 'varfim']
Gramatica = {1:["P\'",["P"]],
             2:["P",["inicio","V", "A"]],   
             3:["V",["varinicio","LV"]],   
             4:["LV",["D", "LV"]],   
             5:["LV",["varfim",";"]],   
             6:["D" ,["id", "TIPO",";"]],   
             7:["TIPO",["inteiro"]],   
             8:["TIPO",["real"]],   
             9:["TIPO",["lit"]],
             10:["A",["ES", "A"]],   
             11:["ES",["leia","id",";"]],   
             12:["ES",["escreva","ARG",";"]],   
             13:["ARG",["literal"]],   
             14:["ARG",["num"]],   
             15:["ARG",["id"]],   
             16:["A",["CMD","A"]],   
             17:["CMD",["id","rcb","LD",";"]],   
             18:["LD",["OPRD","opm","OPRD"]],   
             19:["LD",["OPRD"]],   
             20:["OPRD",["id"]],   
             21:["OPRD",["num"]],   
             22:["A",["COND","A"]],   
             23:["COND",["CABECALHO","CORPO"]],   
             24:["CABECALHO",["se","(","EXP_R",")","entao"]],   
             25:["EXP_R",["OPRD","opr","OPRD"]],   
             26:["CORPO",["ES","CORPO"]],   
             27:["CORPO",["CMD","CORPO"]],   
             28:["CORPO",["COND","CORPO"]],   
             29:["CORPO",["fimse"]],   
             30:["A",["fim"]]}

def Apresentar(linha,coluna,estado,token,ACTION,TabelaDeErros):
    if token == 'ERRO':
        print('ERRO LEXICO: Token Invalido na linha '+ str(linha) + ' coluna ' + str(coluna))
        return
    mensagem = 'ERRO SINTATICO:'
    erro = int(ACTION[estado][token][1:])
    for item in TabelaDeErros[erro]:
        if not(pd.isnull(TabelaDeErros[erro][item])):
            mensagem = mensagem + '{'+ str(TabelaDeErros[erro][item]) + '}'
    mensagem = mensagem + ' esperado antes de linha ' + str(linha) + ' coluna ' + str(coluna)
    print(mensagem)

def Recuperar(token,a,AnalisadorLexico,pilha,ACTION,GOTO,TabelaDeErros):
    while(1):
        s = pilha[-1]
        if ACTION[s][token][0] == 's':
            t = int(ACTION[s][token][1:])
            pilha.append(t)
            if token == a.token:
                a = AnalisadorLexico.getToken()
                token = a.token
            token = a.token
            break
        elif ACTION[s][token][0] == 'r':
            regra = int(ACTION[s][token][1:])
            A,Beta = Gramatica[regra]
            for cont in range(0,len(Beta)):
                if len(pilha) <= 0:
                    break
                pilha.pop()
            t = pilha[-1]
            pilha.append(int(GOTO[t][A]))
            if token == a.token:
                break        
        else:
            if a.token == 'ERRO':
                print('ERRO LEXICO: Token Invalido na linha '+ str(AnalisadorLexico.linha) + ' coluna ' + str(AnalisadorLexico.coluna))
                a = AnalisadorLexico.getToken()
                break
            else:
                return (None,None,None,False)
    return(pilha,a,token,True)
        

def AnaliseSintatica(AnalisadorLexico):
    ACTION = pd.read_csv("ACTIONNEW.csv",sep=';',index_col='Estados')
    ACTION = pd.DataFrame.to_dict(ACTION,orient='index')
    GOTO = pd.read_csv("GOTO.csv",sep=';',index_col='Estados')
    GOTO = pd.DataFrame.to_dict(GOTO,orient='index')
    TabelaDeErros = pd.read_csv("MENSAGEM_ERROS.csv",sep=';',index_col='CodErro')
    TabelaDeErros = pd.DataFrame.to_dict(TabelaDeErros,orient='index')
    
    a = AnalisadorLexico.getToken()
    pilha = [0]
    while(1):
        s = pilha[-1]
        if a.token != 'ERRO' and ACTION[s][a.token][0] == 's':
            t = int(ACTION[s][a.token][1:])
            pilha.append(t)
            a = AnalisadorLexico.getToken()
        elif a.token != 'ERRO' and ACTION[s][a.token][0] == 'r':
            regra = int(ACTION[s][a.token][1:])
            A,Beta = Gramatica[regra]
            for cont in range(0,len(Beta)):
                if len(pilha) <= 0:
                    break
                pilha.pop()
            t = pilha[-1]
            pilha.append(int(GOTO[t][A]))
            print(A+' -> '+' '.join(Beta))
        elif a.token != 'ERRO' and ACTION[s][a.token] == 'acc':
            regra = 1
            A,Beta = Gramatica[regra]
            for cont in range(0,len(Beta)):
                if len(pilha) <= 0:
                    break
                pilha.pop()
            t = pilha[-1]
            print(A+' -> '+' '.join(Beta))
            break
        else:
            """
                Tratamento de erros, criar nova classe e centralizar os erros léxicos e sintáticos lá
            """
            if a.token == 'ERRO':
                print('ERRO LEXICO: Token Invalido na linha '+ str(AnalisadorLexico.linha) + ' coluna ' + str(AnalisadorLexico.coluna))
                a = AnalisadorLexico.getToken()
            else: 
                mensagem = 'ERRO SINTATICO:'
                erro = int(ACTION[s][a.token][1:])
                
                for item in TabelaDeErros[erro]:
                    if not(pd.isnull(TabelaDeErros[erro][item])):
                        mensagem = mensagem + '{'+ str(TabelaDeErros[erro][item]) + '}'
                mensagem = mensagem + ' esperado antes de linha ' + str(AnalisadorLexico.linha) + ' coluna ' + str(AnalisadorLexico.coluna)
                print(mensagem)
                token = ''
                for item in TabelaDeErros[erro]:
                    if not(pd.isnull(TabelaDeErros[erro][item])):
                        token = str(TabelaDeErros[erro][item])
                        pilhaResult,aResult,tokenResult,recuperado = Recuperar(token,a,AnalisadorLexico,pilha,ACTION,GOTO,TabelaDeErros)
                        if pilhaResult != None:
                            pilha = pilhaResult
                            a = aResult
                            #print(a.token,pilha)
                            break
if __name__ == "__main__":
    TabelaDeSimbolos = TabelaDeSimbolos()
    TabelaDeSimbolos.PreencheHashComPalavrasReservadas()
    arquivo = sys.argv[1]
    AnalisadorLexico = Lexico(arquivo,TabelaDeSimbolos.Tabela)
    AnaliseSintatica(AnalisadorLexico)