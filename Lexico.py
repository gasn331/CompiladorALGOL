from AFD import AFD
from Palavra import Palavra
from TabelaDeSimbolos import TabelaDeSimbolos
import string
import re

"""
    Léxico recebe o endereço do código fonte a ser analisado como entrada,
    executa o autômato sobre a entrada e retorna uma estrutura do tipo Palavra com um token.
"""
class Lexico:
    def __init__(self,arquivo,TabelaDeSimbolos):
        self.arquivo  = arquivo
        self.coluna   = 0
        self.linha    = 1
        self.TabelaDeSimbolos = TabelaDeSimbolos
    """
        O método BuscaToken executa o AFD sobre a entrada e retorna um token ou um erro.
        O resultado do autômato(explicado em AFD.py) é armazenado em um objeto Palavra que
        armazena o lexema, token e tipo, e então retornado o token reconhecido.
        Como a função deve retornar alguma coisa, executar de AFD pode retornar uma cadeia vazia
        no caso de espaços vazios e quebras de linha(de acordo com as regras do python).
        Portanto, se o lexema for '' então o léxico retorna None(correspondente de null).
    """
    def BuscaToken(self):
        automato = AFD(self.arquivo,0,self.linha,self.coluna)
        aceito,lexema,token,linhaToken,colunaToken = automato.executar()
        self.linha = automato.linha
        self.coluna = automato.coluna
        if lexema != '':
            if aceito:
                palavra = Palavra(lexema,token,'-')
                if palavra.lexema == 'lit':
                    palavra.tipo = palavra.lexema
                elif palavra.lexema == 'inteiro':
                    palavra.tipo = 'int'
                elif palavra.lexema == 'real':
                    palavra.tipo = 'double'
                elif palavra.token == 'opm' or palavra.token == 'opr':
                    palavra.tipo = palavra.lexema
                elif palavra.token == 'rcb':
                    palavra.tipo = '='
                else:
                    if palavra.token == 'num':
                        if palavra.lexema.find('.') != -1:
                            palavra.tipo = 'double'
                        else:
                            palavra.tipo = 'int'
                    if palavra.token == 'literal':
                        palavra.tipo = 'literal'
            else:
                palavra = Palavra('Token Invalido na linha '+ str(linhaToken) + ' coluna ' + str(colunaToken),'ERRO','-')
            return palavra
        return None
    
    def getToken(self):
        a = self.BuscaToken()
        if a != None and a.token == 'comentario':
            a = self.BuscaToken()
        if a == None:
            a = self.BuscaToken()
            while a == None:
                a = self.BuscaToken()
        if a.token == 'id':
            if a.lexema in self.TabelaDeSimbolos:
                a = self.TabelaDeSimbolos[a.lexema]
            else:
                self.TabelaDeSimbolos[a.lexema] = a
        return a
        