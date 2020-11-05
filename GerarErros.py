import pandas as pd

OPERADORES_ARITMETICOS = ['+','-','*','/']
OPERADORES_RELACIONAIS = ['>','<','=','<>','<=','>=']
ATRIBUICAO = ['<-']
PT_V = [';']


def PreencheACTION(ACTION):
    ACTION = ACTION
    for estado in range(0,len(ACTION)):
        for terminal in ACTION[estado]:
            if not(pd.isnull(ACTION[estado][terminal])):
                ACTION[estado][terminal] = 1
    return ACTION

def PercorrerTabela():
    CodigoDeErro = {0:[0]}
    ACTION = pd.read_csv("ACTION.csv",sep=';',index_col='Estados')
    ACTION = pd.DataFrame.to_dict(ACTION,orient='index')

    for estado in range(0,len(ACTION)):
        erroEncontrado = False
        CodigoEstado = -1
        for erro in CodigoDeErro:
            if estado in CodigoDeErro[erro]:
                erroEncontrado = True
                CodigoEstado = erro
        if not erroEncontrado:
            cont = 0
            for estado2 in range(0,len(ACTION)):
                if estado != estado2 and ACTION[estado] == ACTION[estado2]:
                    cont = cont+1
                    CodigoEstado2 = -1
                    erroEncontrado2 = False
                    for erro in CodigoDeErro:
                        if estado2 in CodigoDeErro[erro]:
                            erroEncontrado2 = True
                            CodigoEstado2 = erro
                    if erroEncontrado2:
                        CodigoDeErro[CodigoEstado2].append(estado)
                    else:
                        lst = list(CodigoDeErro)
                        #print(lst[-1])
                        CodigoDeErro[lst[-1]+1] = [estado,estado2]
            if cont == 0:
                lst = list(CodigoDeErro)
                #print(lst[-1])
                CodigoDeErro[lst[-1]+1] = [estado]
        else:
            for estado2 in range(0,len(ACTION)):
                if estado != estado2 and ACTION[estado] == ACTION[estado2]:
                    CodigoEstado2 = -1
                    erroEncontrado2 = False
                    for erro in CodigoDeErro:
                        if estado2 in CodigoDeErro[erro]:
                            erroEncontrado2 = True
                            CodigoEstado2 = erro
                    if erroEncontrado2:
                        CodigoDeErro[CodigoEstado2].remove(estado2)
                        if len(CodigoDeErro[CodigoEstado2]) == 0:
                            del CodigoDeErro[CodigoEstado2]
                    if not(estado2 in CodigoDeErro[CodigoEstado]):
                        CodigoDeErro[CodigoEstado].append(estado2)
    return CodigoDeErro,ACTION

def PreencheErrosEmACTION(CodigoDeErro,ACTION):
    for erro in CodigoDeErro:
        for estado in CodigoDeErro[erro]:
            for terminal in ACTION[estado]:
                if pd.isnull(ACTION[estado][terminal]):
                    ACTION[estado][terminal] = 'e'+str(erro)
    
    return ACTION

def SalvaACTION(ACTION):
    DF_ACTION = pd.DataFrame.from_dict(ACTION,orient='index')
    pd.DataFrame(DF_ACTION).to_csv("ACTIONNEW.csv",sep=';',index='Estados')

def SalvaTokensErro(CodigoDeErro,ACTION):
    ErroComTokens = {}
    for key,value in CodigoDeErro.items():
        estado = value[0]
        ErroComTokens[key] = []
        for token in ACTION[estado]:
            if not(pd.isnull(ACTION[estado][token])):
                ErroComTokens[key].append(token)
    print(ErroComTokens)
    DF_ERROS = pd.DataFrame.from_dict(ErroComTokens,orient='index')
    pd.DataFrame(DF_ERROS).to_csv("MENSAGEM_ERROS.csv",sep=';')

    
if __name__ == "__main__":
    CodigoDeErro,ACTION = PercorrerTabela()
    SalvaTokensErro(CodigoDeErro,ACTION)
    ACTION = PreencheErrosEmACTION(CodigoDeErro,ACTION)
    SalvaACTION(ACTION)
