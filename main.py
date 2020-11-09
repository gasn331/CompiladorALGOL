from Lexico import Lexico
import pandas as pd
import sys
from TabelaDeSimbolos import TabelaDeSimbolos
"""
Execucao: python main.py [Arquivo de entrada]
"""
AConj = ["P","V","A","CORPO","EXP_R","COND","ES","D","CABECALHO","LV","CMD"]
FollowAConj = { "P":["$"],
                 "V":["fim","leia","escreva","id","se"],
                 "A":["$"],
                 "EXP_R":[")"],
                 "COND":["fim","leia","escreva","id","se","fimse"],
                 "ES":["fim","leia","escreva","id","se","fimse"],
                 "D":["varfim","id"],
                 "CABECALHO":["leia","escreva","id","se","fimse"],
                 "CORPO":["fim","leia","escreva","id","se","fimse"],
                 "LV": ["fim","leia","escreva","id","se"],
                 "CMD": ["fim","leia","escreva","id","se","fimse"]}

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
                --------------Tratamento de erros------------
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
                while(1):
                    NewState = -1
                    NewNonTerminal = ''
                    AnalisadorBacked = AnalisadorLexico
                    aBacked = a
                    while (1):
                        s = pilha[-1]
                        for NaoTerminal in GOTO[s]:
                            if not(pd.isnull(GOTO[s][NaoTerminal])) and NaoTerminal in AConj:
                                NewState = GOTO[s][NaoTerminal]
                                NewNonTerminal = NaoTerminal
                                break
                        if NewState < 0:
                            pilha.pop()
                        else:
                            pilha.append(int(NewState))
                            break
                    while(1):
                        if a.token in FollowAConj[NewNonTerminal]:
                            break
                        if a.token == '$':
                            break
                        a = AnalisadorLexico.getToken()
                    if a.token != "fim" and a.token in FollowAConj[NewNonTerminal]:
                        break
                    else:
                        pilha.pop()
                        pilha.pop()
                        AnalisadorLexico = AnalisadorBacked
                        a = aBacked

            

if __name__ == "__main__":
    TabelaDeSimbolos = TabelaDeSimbolos()
    TabelaDeSimbolos.PreencheHashComPalavrasReservadas()
    arquivo = sys.argv[1]
    AnalisadorLexico = Lexico(arquivo,TabelaDeSimbolos.Tabela)
    AnaliseSintatica(AnalisadorLexico)