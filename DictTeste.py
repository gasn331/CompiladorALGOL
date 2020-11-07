estrutura = {0:['A',[1,2,3]],
             1:['A',[4,5,6]]}

key,value = estrutura[0]
print(key,value)
print(len(value)


delim = False
                    for item in TabelaDeErros[erro]:
                        if not(pd.isnull(TabelaDeErros[erro][item])) and (TabelaDeErros[erro][item] in Delimitador):
                            a.token = str(TabelaDeErros[erro][item])
                            delim = True
                            break
                    while ACTION[s][a.token][0] == 'e' and not delim:
                        a = AnalisadorLexico.getToken()
                        print(a.token)
            """Apresentar(AnalisadorLexico.linha,AnalisadorLexico.coluna,pilha[-1],a.token,ACTION,TabelaDeErros)
            for item in ACTION[pilha[-1]]:
                if ACTION[pilha[-1]][item][0] != 'e':
                    pilha,a,_,recuperado = Recuperar(item,a,AnalisadorLexico,pilha,ACTION,GOTO,TabelaDeErros)
                    if recuperado:
                        break"""
        
