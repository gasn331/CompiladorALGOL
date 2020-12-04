from Palavra import Palavra
from PalavraExtend import PalavraExt
from TabelaDeSimbolos import TabelaDeSimbolos
from Lexico import Lexico        

class Semantico:
    def __init__(self,Gramatica):
        self.VariavelTemporariaCount = 0
        self.ArquivoIntermediarioC = open("temp.c","w")
        self.ArquivoFinal = open("output.c","w")
        self.ArquivoFinal.write("#include<stdio.h>\ntypedef char lit[256];\nvoid main(void)\n{\n\t/*----Variaveis temporarias----*/\n")
        self.Gramatica = Gramatica
        self.escopo    = 0
    
    def five(self,pilhaSemantica,token,AnalisadorLexico):
        self.ArquivoIntermediarioC.write("\n\n\n")
    
    def six(self,pilhaSemantica,token,AnalisadorLexico):
        while (pilhaSemantica) and (pilhaSemantica[-1].token != 'TIPO'):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        TIPO = pilhaSemantica[-1]
        pilhaSemantica.pop()
        
        while (pilhaSemantica) and (pilhaSemantica[-1].token != 'id'):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        ID = pilhaSemantica[-1]
        pilhaSemantica.pop()
        
        AnalisadorLexico.TabelaDeSimbolos[ID.lexema].tipo = TIPO.tipo
        for _ in range(0,self.escopo):
            self.ArquivoIntermediarioC.write("\t")
        self.ArquivoIntermediarioC.write(TIPO.tipo + " " + ID.lexema + ";\n")
         

    def seven(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].lexema != 'inteiro')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        TIPO = PalavraExt("TIPO","TIPO","int",pilhaSemantica[-1].linha,pilhaSemantica[-1].coluna)
        pilhaSemantica.pop()
        pilhaSemantica.append(TIPO)
        return
    
    def eight(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].lexema != 'real')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        TIPO = PalavraExt("TIPO","TIPO","double",pilhaSemantica[-1].linha,pilhaSemantica[-1].coluna)
        pilhaSemantica.pop()
        pilhaSemantica.append(TIPO)
        return
    
    def nine(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].lexema != 'lit')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        TIPO = PalavraExt("TIPO","TIPO","lit",pilhaSemantica[-1].linha,pilhaSemantica[-1].coluna)
        pilhaSemantica.pop()
        pilhaSemantica.append(TIPO)
        return
        
    def eleven(self,pilhaSemantica,token,AnalisadorLexico):
        ID = ''
        while (pilhaSemantica) and (pilhaSemantica[-1].token != 'id'):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        ID = pilhaSemantica[-1].lexema
        pilhaSemantica.pop()
        Variavel = AnalisadorLexico.TabelaDeSimbolos[ID]
        if Variavel.tipo != '-':
            for _ in range(self.escopo):
                self.ArquivoIntermediarioC.write("\t")
            if Variavel.tipo == 'int':
               self.ArquivoIntermediarioC.write("scanf(\"%d\", &"+Variavel.lexema+");\n") 
            elif Variavel.tipo == 'double':
                self.ArquivoIntermediarioC.write("scanf(\"%lf\", &"+Variavel.lexema+");\n")
            else:
                self.ArquivoIntermediarioC.write("scanf(\"%s\", "+Variavel.lexema+");\n")
        else:
            print("ERRO SEMANTICO: Variavel nao declarada na linha "+ str(ID.linha) + " coluna " + str(ID.coluna) +".\n")

    
    def twelve(self,pilhaSemantica,token,AnalisadorLexico):
        while (pilhaSemantica) and (pilhaSemantica[-1].token != 'ARG'):
                pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        ARG = pilhaSemantica[-1]
        pilhaSemantica.pop()

        for _ in range(self.escopo):
            self.ArquivoIntermediarioC.write("\t")
        if ARG.tipo == 'literal':
            self.ArquivoIntermediarioC.write("printf("+ARG.lexema+");\n")
        elif ARG.tipo == 'int':
            self.ArquivoIntermediarioC.write("printf(\"%d\","+ARG.lexema+");\n")
        elif ARG.tipo == 'double':
            self.ArquivoIntermediarioC.write("printf(\"%lf\","+ARG.lexema+");\n")
        elif ARG.tipo == 'lit':
            self.ArquivoIntermediarioC.write("printf(\"%s\","+ARG.lexema+");\n")

    
    def thirteen(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'literal')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        literal = pilhaSemantica[-1]
        pilhaSemantica.pop()
        ARG = PalavraExt(literal.lexema,"ARG",literal.tipo,literal.linha,literal.coluna)
        pilhaSemantica.append(ARG)
        
    def fourteen(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'num')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        num = pilhaSemantica[-1]
        pilhaSemantica.pop()
        ARG = PalavraExt(num.lexema,"ARG",num.tipo,num.tipo,num.coluna)
        pilhaSemantica.append(ARG)

    def fifteen(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'id')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        ID = pilhaSemantica[-1]
        pilhaSemantica.pop()
        if ID.tipo != '-':
            ARG = PalavraExt(ID.lexema,"ARG",ID.tipo,ID.linha,ID.coluna)
            pilhaSemantica.append(ARG)
        else:
            print("ERRO SEMANTICO: Variavel nao declarada na linha "+ str(ID.linha) + " coluna " + str(ID.coluna) +".\n")

    def seventeen(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'LD')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        LD = pilhaSemantica[-1]
        pilhaSemantica.pop()

        while(pilhaSemantica and (pilhaSemantica[-1].token != 'rcb')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        rcb = pilhaSemantica[-1]
        pilhaSemantica.pop()

        while(pilhaSemantica and (pilhaSemantica[-1].token != 'id')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        ID = pilhaSemantica[-1]
        pilhaSemantica.pop()
        if ID.tipo != '-':
            if ID.tipo == LD.tipo:
                for _ in range(self.escopo):
                    print("\t")
                self.ArquivoIntermediarioC.write(ID.lexema + rcb.tipo + LD.lexema + ';\n')
            else:
                print("ERRO SEMANTICO: Tipos diferentes para atribuicao na linha "+ str(LD.linha) + " coluna " + str(LD.coluna) +".\n")    
        else:
            print("ERRO SEMANTICO: Variavel nao declarada na linha "+ str(ID.linha) + " coluna " + str(ID.coluna) +".\n")

    def eighteen(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'OPRD')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        OPRDDir = pilhaSemantica[-1]
        pilhaSemantica.pop()

        while(pilhaSemantica and (pilhaSemantica[-1].token != 'opm')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        opm = pilhaSemantica[-1]
        pilhaSemantica.pop()

        while(pilhaSemantica and (pilhaSemantica[-1].token != 'OPRD')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        OPRDEsq = pilhaSemantica[-1]
        pilhaSemantica.pop()

        if OPRDEsq.tipo != 'literal' and OPRDEsq.tipo == OPRDDir.tipo:
            LD = PalavraExt('T'+ str(self.VariavelTemporariaCount),"LD",OPRDEsq.tipo,OPRDEsq.linha,OPRDEsq.coluna)
            pilhaSemantica.append(LD)
            self.VariavelTemporariaCount = self.VariavelTemporariaCount+1
            for _ in range(self.escopo):
                self.ArquivoIntermediarioC.write("\t")
            """
            Talvez seja melhor criar dois arquivos e fazer uma junção ao final,
            esse método aqui pode dar problema mais pra frente.
            """
            self.ArquivoFinal.write("\t"+OPRDEsq.tipo+' '+LD.lexema+';\n')
            self.ArquivoIntermediarioC.write(LD.lexema + '=' + OPRDEsq.lexema + opm.tipo + OPRDDir.lexema+';\n')
        else:
             print("ERRO SEMANTICO: Operandos com tipos incompativeis na linha "+ str(OPRDEsq.linha) + " coluna " + str(OPRDEsq.coluna) +".\n")

    def nineteen(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'OPRD')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        OPRD = pilhaSemantica[-1]
        pilhaSemantica.pop()

        LD = PalavraExt(OPRD.lexema,"LD", OPRD.tipo, OPRD.linha, OPRD.coluna)
        pilhaSemantica.append(LD)

    def twenty(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'id')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        ID = pilhaSemantica[-1]
        pilhaSemantica.pop()

        OPRD = PalavraExt(ID.lexema,"OPRD", ID.tipo, ID.linha, ID.coluna)
        pilhaSemantica.append(OPRD)

    def twentyone(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'num')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        num = pilhaSemantica[-1]
        pilhaSemantica.pop()

        OPRD = PalavraExt(num.lexema,"OPRD", num.tipo, num.linha, num.coluna)
        pilhaSemantica.append(OPRD)


    def twentythree(self,pilhaSemantica,token,AnalisadorLexico):
        for _ in range(self.escopo-1):
            self.ArquivoIntermediarioC.write("\t")
        self.ArquivoIntermediarioC.write("}\n")
        self.escopo = self.escopo - 1

    def twentyfour(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'EXP_R')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        EXP_R = pilhaSemantica[-1]
        pilhaSemantica.pop()
        for _ in range(self.escopo):
            self.ArquivoIntermediarioC.write("\t")
        self.ArquivoIntermediarioC.write("if("+EXP_R.lexema+")\n")
        for _ in range(self.escopo):
            self.ArquivoIntermediarioC.write("\t")
        self.ArquivoIntermediarioC.write("{\n")
        self.escopo = self.escopo + 1
        

    def twentyfive(self,pilhaSemantica,token,AnalisadorLexico):
        while(pilhaSemantica and (pilhaSemantica[-1].token != 'OPRD')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        OPRDDir = pilhaSemantica[-1]
        pilhaSemantica.pop()

        while(pilhaSemantica and (pilhaSemantica[-1].token != 'opr')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        opr = pilhaSemantica[-1]
        pilhaSemantica.pop()

        while(pilhaSemantica and (pilhaSemantica[-1].token != 'OPRD')):
            pilhaSemantica.pop()
        if not pilhaSemantica:
            return
        OPRDEsq = pilhaSemantica[-1]
        pilhaSemantica.pop()

        if(OPRDEsq.tipo == 'int' or OPRDEsq.tipo == 'double') and (OPRDDir.tipo == 'int' or OPRDDir.tipo == 'double'):
            EXP_R = PalavraExt('T'+ str(self.VariavelTemporariaCount),"EXP_R","int",OPRDEsq.linha,OPRDEsq.coluna)
            self.VariavelTemporariaCount = self.VariavelTemporariaCount+1
            pilhaSemantica.append(EXP_R)
            for _ in range(self.escopo):
                self.ArquivoIntermediarioC.write("\t")
            self.ArquivoFinal.write("\tint "+EXP_R.lexema+';\n')
            self.ArquivoIntermediarioC.write(EXP_R.lexema + '=' + OPRDEsq.lexema + opr.tipo +  OPRDDir.lexema+';\n')
        else:
            print("ERRO SEMANTICO: Operandos com tipos incompativeis na linha "+ str(OPRDEsq.linha) + " coluna " + str(OPRDEsq.coluna) +".\n")

    def executar(self,pilhaSemantica,regra,token,AnalisadorLexico):
        """Nesse ponto devo buscar a regra semântica correspondente à regra da redução,
        e então executar as ações de acordo com a proposta do trabalho T3."""
        switcher = {
            5: self.five,
            6: self.six,
            7: self.seven,
            8: self.eight,
            9: self.nine,
            11: self.eleven,
            12: self.twelve,
            13: self.thirteen,
            14: self.fourteen,
            15: self.fifteen,
            17: self.seventeen,
            18: self.eighteen,
            19: self.nineteen,
            20: self.twenty,
            21: self.twentyone,
            23: self.twentythree,
            24: self.twentyfour,
            25: self.twentyfive
        }
        # Get the function from switcher dictionary
        func = switcher.get(regra)
        # Execute the function
        if func:
            func(pilhaSemantica,token,AnalisadorLexico)


