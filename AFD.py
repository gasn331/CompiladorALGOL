from Palavra import Palavra
import re
import linecache

"""
O AFD utiliza um dicionário para construir o autômato, cada linha do dicionário armazena elementos que representam,
respectivamente, o estado adjacente ao estado atual e seus caracteres de transição. No caso de mais de um elemento na transição de um estado para o outro
estão sendo utilizadas expressões regulares para determinar a função de transição de um estado para o outro ex:[a-zA-Z] para determinar letras.

A lista de aceitação representa os estados de aceitação do autômato, essa lista é representada por pares (estado,token) para poder
determinar quais os tokens reconhecidos de acordo com o estado.

Os casos de erro são determinados a partir de finalização da execução do automato num estado que não seja de aceitação.
Assim, a construção do autômato é simplificada.
"""

class AFD:
    def __init__(self,arquivo,inicial,linha,coluna):
        self.arquivo   = arquivo 
        self.inicial   = inicial
        self.linha     = linha
        self.coluna    = coluna
        self.aceitacao = {1:'Num',3:'Num',6:'Num',7:'OPM',9:'Literal',10:'id',12:'Comentario',13:'EOF',14:'OPR',15:'OPR',16:'OPR',17:'RCB',18:'OPR',19:'FC_P',20:'AB_P',21:'PT_V'}
        self.afd       = {0: {1:'[0-9]',7:r'[\+|\-|\/|\*]',8:r'\"',10:'[a-zA-Z]', 11: r'\{', 13:r'\$',14:r'\>',16:r'\<',18:r'\=',19:r'\)',20:r'\(',21:r'\;'},
                          1: {1:'[0-9]', 2:r'\.',4:'[e|E]',6:'[0-9]'},
                          2: {3:'[0-9]'},
                          3: {4:'[e|E]',6:'[0-9]'},
                          4: {5:r'\+|\-',6:'[0-9]'},
                          5: {6:'[0-9]'},
                          6: {6:'[0-9]'},
                          7: {},
                          8: {8:r'[^\"\n]',9:r'\"'},
                          9: {},
                          10: {10:r'[a-zA-Z|0-9|\_]'},
                          11: {11:r'[^\}\n]',12:r'\}'},
                          12: {},
                          13: {},
                          14: {15:'='},
                          15: {},
                          16: {15:'[>|=]',17:r'\-'},
                          17: {},
                          18: {},
                          19: {},
                          20: {},
                          21: {}}
    def executar(self):
        linhaToken = colunaToken = 0
        """
        Linecache.getline lê o arquivo de entrada linha por linha ao invés de carregar o arquivo inteiro de uma vez, economizando memória.
        """
        cadeia = linecache.getline(self.arquivo, self.linha)
        if cadeia == '':
            cadeia = '$'
            """ 
            $ é utilizado como escape para fim de arquivo,
            python não retorna EOF ao terminar a leitura de arquivo,
            apenas cadeia vazia, nesse caso, utilizo $ para finalizar o arquivo.
            """
        estado = self.inicial
        coluna = self.coluna
        tokenAvaliado = []
        token = ''
        """
        No laço mais externo a cadeia de entrada é percorrida caracter a caracter,
        executando o autômato sobre o caracter determinado.
        """
        for c in range(coluna,len(cadeia)):
            coluna = c
            """
            Partindo de estado(acima determinado como estado inicial) uma vez que cada execução retorna um
            token, é percorrida a lista de estados adjacentes com entrada cadeia[c], representando o caracter atual
            do arquivo.
            """
            if len(self.afd[estado]) == 0:
                break
            for index,adjacente in enumerate(self.afd[estado]):
                """
                query recebe a transição do estado(atual) para um estado adjacente,
                a lista de estados adjacentes é percorrida a fim de encontrar uma transição
                que leia cadeia[c] como entrada e vá para outro estado.
                """
                query = self.afd[estado][adjacente]
                """
                Caso haja correspondência entre query e o caracter atual(cadeia[c])
                o estado atual passa para o estado adjacente, e tokenAvaliado adiciona o caracter à sua lista.
                """
                if re.match(query, cadeia[c]):
                    estado = adjacente
                    tokenAvaliado.append(cadeia[c])
                    break
                else:
                    """
                    Caso não haja correspondência entre o caracter atual e alguma transição para outro estado,
                    confirma-se se o estado atual é de aceitação, ou seja, se um token foi reconhecido.
                    Caso seja uma quebra de linha, a linha atual é atualizada para a seguinte e a coluna zerada.
                    Cso seja um espaço vazio, a coluna atual é atualizada para a próxima, para que a execução,
                    ao ser reiniciada, possa continuar a partir do próximo caracter.
                    """
                    if estado in self.aceitacao and index == len(self.afd[estado])-1:
                        self.coluna = c
                        linhaToken = self.linha
                        colunaToken = self.coluna
                        if cadeia[c] == '\n':
                            self.linha = self.linha+1
                            self.coluna = 0
                        if cadeia[c] == ' ':
                            self.coluna = c+1
                        token = ''
                        if estado in self.aceitacao:
                            token = self.aceitacao[estado]
                        return (estado in self.aceitacao,''.join(tokenAvaliado),token,linhaToken,colunaToken)
            coluna = c
            """
            Captura de erro no código fonte passado como entrada. O erro é avaliado a partir do critério de:
            se um estado de aceitação não foi alcançado e o caracter atual não foi adicionado ao tokenAvaliado.
            Nesse caso, ao invés de retornar o lexema e token, é retornado ERRO para representar estado de erro
            e a indicação da linha e coluna em que o erro foi encontrado.
            """
            if not(cadeia[c] in tokenAvaliado) and cadeia[c] != '\n' and cadeia[c] != ' ':
                self.coluna = c+1
                linhaToken = self.linha
                colunaToken = c
                return(cadeia[c] in tokenAvaliado,'ERRO','',linhaToken,colunaToken)
            if cadeia[c] == '\n':
                token = ''
                linhaToken = self.linha
                colunaToken = self.coluna
                self.linha = self.linha+1
                self.coluna = 0
                if estado in self.aceitacao:
                    token = self.aceitacao[estado]
                return (estado in self.aceitacao,''.join(tokenAvaliado),token,linhaToken,colunaToken)
                #    return(False,'ERRO','Token Invalido na linha '+ str(self.linha-1) + ' coluna ' + str(c))

        """
        Ao final da execução, retorna-se true ou false para determinar se um estado de aceitação foi alcançado,
        o lexema encontrado(a partir da junção da lista tokenAvaliado) e o token à qual o lexema pertence(caso tenha sido aceito).
        """    
        self.coluna = coluna
        linhaToken = self.linha
        colunaToken = self.coluna
        token = ''
        if estado in self.aceitacao:
            token = self.aceitacao[estado]
        return (estado in self.aceitacao,''.join(tokenAvaliado),token,linhaToken,colunaToken)
        #return(False,'ERRO','Token Invalido na linha '+ str(self.linha) + ' coluna ' + str(coluna))
        
           