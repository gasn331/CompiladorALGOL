from Lexico import Lexico
from Palavra import Palavra
import pandas as pd
import sys
"""
Execucao: python main.py [Arquivo de entrada]
"""
"""
A tabela de símbolos armazena os tokens encontrados em que a chave é o lexema e um objeto Palavra é o valor armazenado.
"""
TabelaDeSimbolos = {}
PalavrasReservadas = ["inicio", "varinicio", "varfim", "escreva",
                      "leia",   "se",        "entao",  "fimse",
                      "fim",    "inteiro",   "lit",    "real"]

"""
1 P' → P
2 P → inicio V A
3 V → varinicio LV
4 LV → D LV
5 LV → varfim;
6 D → id TIPO;
7 TIPO → int
8 TIPO → real
9 TIPO → lit
10 A → ES A
11 ES→leia id;
12 ES→escreva ARG;
13 ARG→literal
14 ARG→num
15 ARG→id
16 A→CMD A
17 CMD→id rcb LD;
18 LD→OPRD opm OPRD
19 LD→OPRD
20 OPRD→id
21 OPRD→num
22 A→COND A
23 COND→CABEÇALHO CORPO
24 CABEÇALHO→se (EXP_R) então
25 EXP_R→OPRD opr OPRD
26 CORPO→ES CORPO
27 CORPO→CMD CORPO
28 CORPO→COND CORPO
29 CORPO→fimse
30 A→fim
"""
Gramatica = {1:["P\'",["P"]],
             2:["P",["inicio","V", "A"]],   
             3:["V",["varinicio","LV"]],   
             4:["LV",["D", "LV"]],   
             5:["LV",["varfim",";"]],   
             6:["D" ,["id", "TIPO",";"]],   
             7:["TIPO",["int"]],   
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
"""
    Essa função preenche a tabela de símbolos com as palavras-chave da linguagem na forma (lexema,token,tipo)
"""
def PreencheHashComPalavrasReservadas():
    for palavraReservada in PalavrasReservadas:
        TabelaDeSimbolos[palavraReservada] = Palavra(palavraReservada,palavraReservada,"-")

def AnaliseSintatica(AnalisadorLexico):
    #ACTION = pd.DataFrame.to_dict(pd.read_csv("ACTION.csv",sep=';'))
    #GOTO = pd.DataFrame.to_dict(pd.read_csv("GOTO.csv",sep=';'))
    ACTION = pd.read_csv("ACTION.csv",sep=';',index_col='Estados')
    ACTION = pd.DataFrame.to_dict(ACTION,orient='index')
    GOTO = pd.read_csv("GOTO.csv",sep=';',index_col='Estados')
    GOTO = pd.DataFrame.to_dict(GOTO,orient='index')
    #pd.DataFrame.set_index('Estados').ACTION
    """print(ACTION)
    print("\n\n\n\n")
    print(GOTO)
    return"""
    a = AnalisadorLexico.BuscaToken()
    if a == None:
        a = AnalisadorLexico.BuscaToken()
        while a == None:
            a = AnalisadorLexico.BuscaToken()

    pilha = [0]
    while(1):
        print(pilha)
        s = pilha[-1]
        pilha.pop()
        if ACTION[s][a.lexema][0] == 's':
            t = int(ACTION[s][a.lexema][1])
            pilha.append(t)
            a = AnalisadorLexico.BuscaToken()
            if a == None:
                a = AnalisadorLexico.BuscaToken()
                while a == None:
                    a = AnalisadorLexico.BuscaToken()
            print('SHIFT')
        elif ACTION[s][a.lexema][0] == 'r':
            regra = int(ACTION[s][a.lexema][1])
            A,Beta = Gramatica[regra]
            for cont in range(0,len(Beta)):
                if len(pilha) <= 0:
                    break
                pilha.pop()
            t = pilha[-1]
            pilha.append(int(GOTO[t][A]))
            print(A+'->'+''.join(Beta))
            print('REDUCE')
        elif ACTION[s][a.lexema] == 'acc':
            #analise completa
            break
        else:
            """
                Tratamento de erros, criar nova classe e centralizar os erros léxicos e sintáticos lá
            """
            pass




if __name__ == "__main__":
    PreencheHashComPalavrasReservadas()
    arquivo = sys.argv[1]
    AnalisadorLexico = Lexico(arquivo)

    AnaliseSintatica(AnalisadorLexico)