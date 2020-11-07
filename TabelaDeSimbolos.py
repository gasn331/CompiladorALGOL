from Palavra import Palavra
"""
A tabela de símbolos armazena os tokens encontrados em que a chave é o lexema e um objeto Palavra é o valor armazenado.
"""
class TabelaDeSimbolos:
    def __init__(self):
        self.Tabela = {}
        self.PalavrasReservadas =  ["inicio", "varinicio", "varfim", "escreva",
                                    "leia",   "se",  "entao",  "fimse",
                                    "fim", "inteiro", "real","lit"]

    def PreencheHashComPalavrasReservadas(self):
        for palavraReservada in self.PalavrasReservadas:
           self.Tabela[palavraReservada] = Palavra(palavraReservada,palavraReservada,"-")