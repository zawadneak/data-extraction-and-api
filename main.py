from zipfile import ZipFile # [1]
import pandas # [2]
import os
from flask import Flask

print("Starting Script...\n")

# STEP 1 - Unzip dados.zip
with ZipFile("dados.zip","r") as dados:
    metadata = dados.infolist()
    print("Extracting Data | {} files".format(len(metadata)))
    for f in metadata:
        print(f.filename)
        dados.extract(f,"")
        
if not os.path.exists("origem-dados.csv") or not os.path.exists("tipos.csv"):
    print("ERROR: Missing required files (origem-dados.csv + tipos.csv). Please check zipped source.")
    exit()
   
print("\nData Extracted.\n")



# STEP 2 + 3 - Read origem-dados and filter status CRITICO
print("\nReading and treating origem-dados...")
origem = pandas.read_csv("origem-dados.csv")
origem = origem[origem["status"]=="CRITICO"]
origem.sort_values("created_at",inplace=True)
print(origem.head())

# STEP 4 - Add nome_tipo based on tipos.csv
# [3]
print("\nAdding nomes_tipo column...")
tipos = pandas.read_csv("tipos.csv")
origem["nomes_tipo"] = tipos.loc[origem["tipo"],"nome"].values
print(origem.head())

# STEP 5 - Generate insert-dados.sql file with data inserts based on origem-dados
# [4]
print("\nGenerating INSERT SQL from origem Dataframe...")
sql_texts = []
for index, row in origem.iterrows():       
    sql_texts.append('INSERT INTO dados_finais ('+ str(', '.join(origem.columns))+ ') VALUES '+ str(tuple(row.values)) + ';')     
with open("insert-dados.sql","x") as f:
    f.write('\n\n'.join(sql_texts))
print("insert-dados.sql file generated.")
    
    
    
# SETP 6 - Item amount by day and type query
# [5]
print("\nItem query (MariaDB):")

query = """
    SELECT DATE_FORMAT(created_at, '%Y-%m-%d') as dia, count(product_code) as qtd, nomes_tipo
        FROM dados_finais
        GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d'),nomes_tipo
    """
print(query)
print("\n\nTo run the Flask API, please run flask --app api.py run")
print("Make your Nome Tipo request at http://localhost:5000/nome-tipo/<tipo_id>")


# references
# [1] => https://docs.python.org/3/library/zipfile.html
# [2] => https://pandas.pydata.org/docs/user_guide/index.html
# [3] => https://pandas.pydata.org/docs/getting_started/intro_tutorials/05_add_columns.html
# [4] => https://stackoverflow.com/questions/31071952/generate-sql-statements-from-a-pandas-dataframe
# [5] => https://stackoverflow.com/questions/508791/mysql-query-group-by-day-month-year