"""
    A classe PalavraExt define um token com as propriedades (lexema,token,tipo) assim como especificado
    nos parâmetros da implementação, porém, adiciona os valores posicionais do token, com linha e coluna.
"""
class PalavraExt:
    def __init__(self, lexema, token, tipo, linha, coluna):
        self.lexema = lexema
        self.token  = token
        self.tipo   = tipo
        self.linha  = linha
        self.coluna = coluna