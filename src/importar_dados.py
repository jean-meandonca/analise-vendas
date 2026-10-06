import pandas as pd

from conexao import engine

#Carregar arquivo CSV
df=pd.read_csv("dados/vendas.csv")

#Converter a coluna de data
df["data"] = pd.to_datetime(df["data"])

#Corrigir categoria
df["categoria"] = df["categoria"].replace(
    "Periféticos",
    "Periféricos"
)

#Enviar os dados para o PostgreSQL
df.to_sql(
    "vendas",
    engine,
    if_exists="replace",
    index=False
)

print(f"{len(df)} registros importados com sucesso!")