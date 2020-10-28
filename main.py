from Lexico import Lexico
from Palavra import Palavra
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
    Essa função preenche a tabela de símbolos com as palavras-chave da linguagem na forma (lexema,token,tipo)
"""
def PreencheHashComPalavrasReservadas():
    for palavraReservada in PalavrasReservadas:
        TabelaDeSimbolos[palavraReservada] = Palavra(palavraReservada,palavraReservada,"-")


if __name__ == "__main__":
    PreencheHashComPalavrasReservadas()
    arquivo = sys.argv[1]
    AnalisadorLexico = Lexico(arquivo)
    """ A seguir deve chamar BuscaToken até EOF"""
    tok = Palavra('','','')
    token = ''
    """
    O AnalisadorLexico retorna um token por vez, assim, ao receber um token, caso seja do tipo 'id' e 
    não exista na tabela de símbolos, ele é adicionado à tabela e impresso na tela, caso exista, apenas é impresso na tela.
    Tokens de outro tipo são apenas impressos na tela.
    """
    while token != 'EOF':
        tok = AnalisadorLexico.BuscaToken()
        if tok != None:
            if tok.token == 'id':
                if not (tok.lexema in TabelaDeSimbolos):
                    TabelaDeSimbolos[tok.lexema] = tok
                else:
                    tok = TabelaDeSimbolos[tok.lexema]
            print(tok.token, tok.lexema,tok.tipo)
            token = tok.token
        else:
            continue