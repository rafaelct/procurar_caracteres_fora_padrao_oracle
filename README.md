# procurar caracteres fora padrao oracle 

Como Instalar:

- Python3
- pip install cx-Oracle

Uso: 

<pre>
python procurar_caracteres_fora_padrao_oracle.py > resultado.csv
Aonde resultado.csv é aonde sera gravado o resultado, depois é só abrir esse arquivo no Excel ou LibreCalc

Como Usar:

Edite o arquivo procurar_caracteres_fora_padrao_oracle.py, e modifique as linhas abaixo dentro do arquivo:

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
    

</pre>

