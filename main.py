from Lexico import Lexico
import pandas as pd
import sys
import os
from TabelaDeSimbolos import TabelaDeSimbolos
from Semantico import Semantico
from PalavraExtend import PalavraExt
"""
Execucao: python main.py [Arquivo de entrada]
"""
"""
AConj é o conjunto de não terminais significativos da gramática,
ou seja, são não terminais cujas produções na gramática tem grande importância na execução.
Dessa forma, o tratamento de erros identifica, de acordo com a escolha de não terminal,
um token pertencente ao follow de determinado não terminal A, assim a execução é retomada após
a detecção de erro.
"""
AConj = ["P","V","A","CORPO","EXP_R","COND","ES","D","CABECALHO","LV","CMD"]
"""
O conjunto FollowAConj contém os conjuntos follow dos não terminais de AConj para 
serem utilizados no tratamento de erros.
"""
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

"""
Gramatica é a gramática da linguagem, utilizada para fazer as reduções no algoritmo shift-reduce.
"""
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
CriarArquivoFInal combina o ArquivoIntermediarioC(temp.c) com os cabeçalhos adequados para o código em C.
"""
def CriarArquivoFinal(AnalisadorSemantico):
    AnalisadorSemantico.ArquivoIntermediarioC.close()
    ArquivoTemporario = open("temp.c","r")
    AnalisadorSemantico.ArquivoFinal.write("\t/*------------------------------*/\n")
    for line in ArquivoTemporario:
        AnalisadorSemantico.ArquivoFinal.write("\t"+line)
    AnalisadorSemantico.ArquivoFinal.write("}")
    AnalisadorSemantico.ArquivoFinal.close()
    ArquivoTemporario.close()
    if os.path.exists("temp.c"):
      os.remove("temp.c")
    

"""
AnaliseSintatica implementa o algoritmo shift-reduce. 
Nessa implementação a Tabela Sintática é dividida em ACTION e GOTO para facilitar o carregamento em estruturas de dados.

ACTIONNEW.csv mantém a tabela ACTION preenchida com códigos de erro.
GOTO.csv mantém a tabela GOTO.
MENSAGEM_ERROS.csv mantém a tabela de erros, cada linha da tabela representa um tipo de erro,
suas colunas representam os tokens esperados na execução do shift-reduce.

A execução do algoritmo segue o algoritmo de shift-reduce, utiliza-se uma pilha para manter os estados.
s é o estado do topo da pilha,
a é o token atual
t representa o estado a ser empilhado
regra representa a regra da gramática a ser utilizada para redução
A e Beta armazenam a regra da gramática, A sendo o lado esquerdo e Beta o lado direito da produção.

Em caso de aceitação é feita mais uma redução para chegar à P'.

Ao ser encontrado um erro léxico, a mensagem de erro é apresentada na tela e um novo token é requisitado ao léxico.

Nessa implementação, ao ser detectado um erro sintático, ele é apresentado na tela
utilizando a TabelaDeErros, o código de erro é extraído da tabela ACTION e a mensagem 
mostra os tokens pertencentes à linha do erro na TabelaDeErros, indicando os tokens esperados.

O método de recuperação de erros utilizado é o Modo Pânico. A recuperação se dá da seguinte forma:
A pilha é escaneada procurando por um estado t em que haja uma transição em GOTO[t,A] cujo
não terminal seja parte do conjunto de não terminais significativos. Ao encontrar esse não terminal,
o estado em GOTO[t,A] é empilhado. A seguir são ignorados tokens da entrada(utilizando AnalisadorLexico.getToken())
até que um token que faça parte do conjunto follow de A seja encontrado, de forma a ignorar o restante do bloco
e retornar a execução para um ponto em que seja possível continuar.

Uma adição feita à esse método foi que caso não seja encontrado um não terminal adequado a partir do estado atual,
o topo da pilha é eliminado, o AnalisadorLexico é retornado à um estado anterior e então é feita a tentativa de recuperação
com o estado atualmente no topo da pilha.
"""
def AnaliseSintatica(AnalisadorLexico):
    ACTION = pd.read_csv("ACTIONNEW.csv",sep=';',index_col='Estados')
    ACTION = pd.DataFrame.to_dict(ACTION,orient='index')
    GOTO = pd.read_csv("GOTO.csv",sep=';',index_col='Estados')
    GOTO = pd.DataFrame.to_dict(GOTO,orient='index')
    TabelaDeErros = pd.read_csv("MENSAGEM_ERROS.csv",sep=';',index_col='CodErro')
    TabelaDeErros = pd.DataFrame.to_dict(TabelaDeErros,orient='index')
    AnalisadorSemantico = Semantico(Gramatica)
    a = AnalisadorLexico.getToken()
    pilha = [0]
    pilhaSemantica = []
    while(1):
        s = pilha[-1]
        if a.token != 'ERRO' and ACTION[s][a.token][0] == 's':
            t = int(ACTION[s][a.token][1:])
            pilha.append(t)
            pilhaSemantica.append(PalavraExt(a.lexema,a.token,a.tipo,AnalisadorLexico.linha,AnalisadorLexico.coluna)) #Adiciona o lexema encontrado na pilha auxiliar do analisador semântico
            a = AnalisadorLexico.getToken()
        elif a.token != 'ERRO' and ACTION[s][a.token][0] == 'r':
            regra = int(ACTION[s][a.token][1:])
            A,Beta = Gramatica[regra]
            for _ in range(0,len(Beta)):
                if len(pilha) <= 0:
                    break
                pilha.pop()
            t = pilha[-1]
            pilha.append(int(GOTO[t][A]))
            print(A+' -> '+' '.join(Beta))
            """
            Chamada para o analisador semântico passando a pilha auxiliar(pilhaSemantica), a regra atual,
            o token atual e uma copia do analisador léxico.
            """
            AnalisadorSemantico.executar(pilhaSemantica,regra,a,AnalisadorLexico)
        elif a.token != 'ERRO' and ACTION[s][a.token] == 'acc':
            regra = 1
            A,Beta = Gramatica[regra]
            for _ in range(0,len(Beta)):
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
    #copiar arquivos de um lado pro outro
    CriarArquivoFinal(AnalisadorSemantico)
            

if __name__ == "__main__":
    TabelaDeSimbolos = TabelaDeSimbolos()
    TabelaDeSimbolos.PreencheHashComPalavrasReservadas()
    arquivo = sys.argv[1]
    AnalisadorLexico = Lexico(arquivo,TabelaDeSimbolos.Tabela)
    AnaliseSintatica(AnalisadorLexico)