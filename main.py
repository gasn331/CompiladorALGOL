from Lexico import Lexico
from Palavra import Palavra
import pandas as pd
import sys
import TratamentoDeErros
"""
Execucao: python main.py [Arquivo de entrada]
"""
"""
A tabela de símbolos armazena os tokens encontrados em que a chave é o lexema e um objeto Palavra é o valor armazenado.
"""
TabelaDeSimbolos = {}
PalavrasReservadas = ["inicio", "varinicio", "varfim", "escreva",
                      "leia",   "se",  "entao",  "fimse",
                      "fim", "inteiro", "real","lit"]

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
Delimitador = [';','fimse','fim',')','$']
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
"""
    Essa função preenche a tabela de símbolos com as palavras-chave da linguagem na forma (lexema,token,tipo)
"""
def PreencheHashComPalavrasReservadas():
    for palavraReservada in PalavrasReservadas:
        TabelaDeSimbolos[palavraReservada] = Palavra(palavraReservada,palavraReservada,"-")

def getToken(AnalisadorLexico):
    a = AnalisadorLexico.BuscaToken()
    if a != None and a.token == 'comentario':
        a = AnalisadorLexico.BuscaToken()
    if a == None:
        a = AnalisadorLexico.BuscaToken()
        while a == None:
            a = AnalisadorLexico.BuscaToken()
    if a.token == 'id':
        if a.lexema in TabelaDeSimbolos:
            a = TabelaDeSimbolos[a.lexema]
    return a


def AnaliseSintatica(AnalisadorLexico):
    ACTION = pd.read_csv("ACTIONNEW.csv",sep=';',index_col='Estados')
    ACTION = pd.DataFrame.to_dict(ACTION,orient='index')
    GOTO = pd.read_csv("GOTO.csv",sep=';',index_col='Estados')
    GOTO = pd.DataFrame.to_dict(GOTO,orient='index')
    
    """print(ACTION)
    print("\n\n\n\n")
    print(GOTO)
    return"""
    a = getToken(AnalisadorLexico)
    pilha = [0]
    while(1):
        #print(pilha)
        s = pilha[-1]
       # print(s,ACTION[s][a.token],a.lexema,a.token)
        if not (pd.isnull(ACTION[s][a.token])) and ACTION[s][a.token][0] == 's':
            t = int(ACTION[s][a.token][1:])
            pilha.append(t)
            a = getToken(AnalisadorLexico)
            #print('SHIFT')
        elif not (pd.isnull(ACTION[s][a.token])) and ACTION[s][a.token][0] == 'r':
            regra = int(ACTION[s][a.token][1:])
            A,Beta = Gramatica[regra]
            for cont in range(0,len(Beta)):
                if len(pilha) <= 0:
                    break
                pilha.pop()
            t = pilha[-1]
            pilha.append(int(GOTO[t][A]))
            print(A+' -> '+' '.join(Beta))
            #print('REDUCE')
        elif not (pd.isnull(ACTION[s][a.token])) and ACTION[s][a.token] == 'acc':
            #analise completa
            break
        else:
            """
                Tratamento de erros, criar nova classe e centralizar os erros léxicos e sintáticos lá
            """
            erro = TratamentoDeErros.Erro(ACTION,Delimitador)
            erro.Apresentar(AnalisadorLexico.linha,AnalisadorLexico.coluna,pilha[-1],a.token)
            a,AnalisadorLexico,pilha = erro.Recuperar(a,AnalisadorLexico,pilha)


if __name__ == "__main__":
    PreencheHashComPalavrasReservadas()
    arquivo = sys.argv[1]
    AnalisadorLexico = Lexico(arquivo)

    AnaliseSintatica(AnalisadorLexico)