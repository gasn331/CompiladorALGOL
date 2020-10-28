"""
    A classe Palavra define um token com as propriedades (lexema,token,tipo) assim como especificado
    nos parâmetros da implementação.
"""
class Palavra:
    def __init__(self, lexema, token, tipo):
        self.lexema = lexema
        self.token  = token
        self.tipo   = tipo