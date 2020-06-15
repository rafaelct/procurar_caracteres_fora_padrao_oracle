import cx_Oracle

def verConexaoDB() :

    # MODIFIQUE AS VARIAVEIS ABAIXO COM OS DADOS DA SUA CONEXÃO
    usuario = "USUARIO"
    senha = "SENHA"
    ipHost = "IP:PORTA/NOMEDOSEVICO"

    # FILTRE AS TABELAS QUE O SCRIPT DEVE PROCURAR POR CARACTERES FORA DO PADRAO, 
    # NÃO ALTERE OS CAMPOS column_name,table_name
    cmdSQLTabelasBuscar = """  SELECT 
    column_name,table_name
FROM   all_tab_cols
WHERE  table_name like '%TB_%' AND DATA_TYPE IN ('CHAR','VARCHAR','VARCHAR2') ORDER BY TABLE_NAME
  """

    # MODIFIQUE PARA DEFINIR OS CARACTERES A DESCONSIDERAR
    caracteresPadrao = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','w','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','W','Y','Z','0','1','2','3','4','5','6','7','8','9',' ',',','.',':','/','-','_','(',';','\\',')']
    
    #### !!!! ATENÇÃO NÃO PRECISA MODIFICAR NADA A PARTIR DAQUI !!!!! ####


    conexao = cx_Oracle.connect(usuario,senha,ipHost)
    cursor = conexao.cursor()

    # Cabecalho do arquivo    
    print("TABELA;NOME DO CAMPO;CARACTERE ESPECIAL ENCONTRADO;VALOR")

    cmdSQLs = buscaTabelas(cursor,cmdSQLTabelasBuscar)

    for sql in cmdSQLs :
        #print(sql)
        cursor.close()
        cursor = conexao.cursor()
        dadosSql = buscaDadosTabela(cursor,sql)

        if dadosSql is None :
            continue

        buscaPadrao(dadosSql,sql,caracteresPadrao)

# Realiza a busca do padrao nos dados vindo do select
def buscaPadrao(dadosSql,sql,caracteresPadrao) :

    #print("-----------------------")
    valorProcurado = []

    for dados in dadosSql:
        resultadoSQL = dados
        #print("busca Padrao:")
        #print(resultadoSQL)
            
        indiceCampo = 0
        #nomeCampoCod = ""
        #campoCod = ""


        for campo in dados :
            #print(campo)
            nomeCampo = sql["campos"][indiceCampo]
            nomeTabela = sql["tabela"]

            #if len(campoCod) == 0 :
            #    nomeCampoCod = nomeCampo
            #    campoCod = str(campo)
            #    indiceCampo += 1
            #    continue

            if campo is None :
                indiceCampo += 1
                continue
            
            # Se a linha tem dado repetido pula para o proximo registro no for
            if valorProcurado.count(nomeTabela+";"+nomeCampo+";"+campo) == 0 :
                valorProcurado.append(nomeTabela+";"+nomeCampo+";"+campo)
            else :

                indiceCampo += 1
                continue

            temAcentos = procurarAcentos(caracteresPadrao,campo)
            if temAcentos["valor"] == False :
                #print("Tem caractere especial.")
                #print("Tabela: "+nomeTabela)
                #print("Nome do Campo: "+nomeCampo)
                #print(" Valor do Campo: "+ campo)
                #print("Caractere especial:"+temAcentos["letra"])
                print(nomeTabela+";"+nomeCampo+";"+temAcentos["letra"]+";"+campo)

            indiceCampo += 1

# Busca dados de uma tabela especificidas
def buscaDadosTabela(cursor,sql) :
    try:
        return cursor.execute(sql["comando"])
    except cx_Oracle.DatabaseError :
        return None

# Busca todas as tabelas do banco de dados de acordo com o padrao informado no select
def buscaTabelas(cursor,sql) :
    cursor.execute(sql)

    tabelaAnterior = ''
    resultado = []
    strCampos = ''
    strResultado = {}

    for dados in cursor :
        campo = dados[0]
        tabela = dados[1]
        

        if tabela != tabelaAnterior and tabelaAnterior != '' :
            resultado.append(strResultado)
            tabelaAnterior = tabela
            strCampos = ''
            strResultado = {}
            
        #if len(strResultado) == 0 :
        #    strCampos = "COD_"+tabela[7:]+","

        if tabelaAnterior == '' :
            tabelaAnterior = tabela
        
        strCampos += campo+","
        strResultado["comando"] = "SELECT DISTINCT " + strCampos[0:-1]+" FROM "+tabela
        strResultado["campos"] = strCampos[0:-1].split(",")
        strResultado["tabela"] = tabela
    
    resultado.append(strResultado)
    return resultado

# procura registros que diferem dos conjuntos de caracteres informados 
def procurarAcentos(caracteresPadrao : list ,txt : str) -> bool :
    #print("Procurando acentos : "+ txt)
    #exemplo:
    #caracteresPadrao = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','w','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','W','Y','Z','0','1','2','3','4','5','6','7','8','9',' ',',','.']
    temPadrao = False
    achei : str
    resultado = {}

    for letra in txt :
        
        achei = letra
        temPadrao = False

        for padrao in caracteresPadrao :
            
            #temPadrao = False
            if letra == padrao :
                temPadrao = True
        
        if temPadrao == False :
            #print("achei :"+letra)
            resultado["letra"] = letra
            resultado["valor"] = temPadrao
            #return temPadrao
            return resultado
        

    resultado["letra"] = ''
    resultado["valor"] = temPadrao
    #return temPadrao
    return resultado

# aqui comeca a execucao   
verConexaoDB()

