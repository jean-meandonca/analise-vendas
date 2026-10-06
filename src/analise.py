import pandas as pd
import matplotlib.pyplot as plt

# ===================================
# CARREGAMENTO 
#====================================
df = pd.read_csv("dados/vendas.csv")

# Dimensões do dataset(tamanho em linhas e colunas: 1000, 78. 1000 linhas e 78 colunas)
print("Dimensões do dataset:")
print(df.shape)

# ===================================
# TRATAMENTO
# ===================================
# Converter data para datetime
df["data"] = pd.to_datetime(df["data"])

# Corrigit categoria
df["categoria"] = df["categoria"].replace(
    "Periféticos",
    "Periféricos"
)

# ==================================
# VALIDAÇÃO
# ==================================

print("\nTipos das colunas:")
print(df.dtypes)

print("\nValores nulos:")
print(df.isnull().sum())

print("\nRegistros duplicados")
print(df.duplicated().sum())

# quantas vezes cada categoria aparece na coluna categoria
print("\nCategorias:")
print(df["categoria"].value_counts())

# ===================================
# ESTATÍSTICAS
# ===================================
# Estatísticas numéricas (calcula algumas informações da tabela como, quantidade de dados(count), média(mean), o valor mínimo (min), (max) etc
print("\nEstatísticas:")
print(df.describe())


# Informações das colunas (quantidade de linhas, colunas, nome das colunas, quantidade de valores nulos em cada coluna, tipo de dado e uso aproximado da memória)
print("\nInformações do dataset pós tratamento")
df.info()

# ===================================
# RESULTADO
# ===================================

print("\nPrimeiros registros:")
print(df.head())

# ===================================
# ANÁLISE DE VENDAS
# ===================================

# Faturamento total
faturamento_total = df["valor_venda"].sum()

print("\nFaturamento total:")
print(f"R$ {faturamento_total:,.2f}")

# Ticket médio
ticket_medio = df["valor_venda"].mean()

print("\nTicket médio:")
print(f"R$ {ticket_medio:,.2f}")

#Faturamento por categoria
faturamento_categoria = (
    df.groupby("categoria")["valor_venda"]
    .sum()
    .sort_values(ascending=False)
)

print("\nFaturamento por categoria:")
print(faturamento_categoria)

#faturamento por produto
faturamento_produto = (
    df.groupby("produto")["valor_venda"]
    .sum()
    .sort_values(ascending=False)
)

print("\nFaturamento por produto:")
print(faturamento_produto)

#Faturamento por região
faturamento_regiao = (
    df.groupby("regiao")["valor_venda"]
    .sum()
    .sort_values(ascending=False)
)

print("\nFaturamento por região")
print(faturamento_regiao)


# ===================================
# ANÁLISE TEMPORAL
# ===================================

df["mes"] = df["data"].dt.to_period("M")

faturamento_mensal = (
    df.groupby("mes")["valor_venda"]
    .sum()
)

print("\nFaturamento por mês:")
print(faturamento_mensal)

# ===================================
# QUANTIDADE POR PRODUTO
# ===================================

quantidade_produto = (
    df.groupby("produto")["quantidade"]
    .sum()
    .sort_values(ascending=False)
)

print("\nQuantidade vendida por produto:")
print(quantidade_produto)

# ===================================
# FATURAMENTO POR PAGAMENTO
# ===================================

faturamento_pagamento = (
    df.groupby("forma_pagamento")["valor_venda"]
    .sum()
    .sort_values(ascending=False)
)

print("\nFaturamento por forma de pagamento:")
print(faturamento_pagamento)


# ===================================
# FATURAMENTO POR CATEGORIA 
# ===================================

faturamento_categoria.plot(kind="bar")

plt.title("Faturamento por Categoria")
plt.xlabel("Categoria")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# ===================================
# FATURAMENTO POR PRODUTO
# ===================================

faturamento_produto.plot(kind="bar")

plt.title("Faturamento por Produto")
plt.xlabel("Produto")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ===================================
# FATURAMENTO POR REGIÃO
# ===================================

faturamento_regiao.plot(kind="barh")

plt.title("Faturamento por Região")
plt.xlabel("Faturamento (R$)")
plt.ylabel("Região")
plt.tight_layout()
plt.show()

# ===================================
# FATURAMENTO MENSAL - evolução do faturamento ao longo dos meses
# ===================================

faturamento_mensal.plot(kind="line", marker="o")

plt.title("Evolução Mensal do Faturamento")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ===================================
# DISTRIBUIÇÃO DO VALOR DAS VENDAS - HISTOGRAMA
# ===================================

df["valor_venda"].plot(kind="hist", bins=30)

plt.title("Distribuição do Valor das Vendas")
plt.xlabel("Valor da Venda (R$)")
plt.ylabel("Quantidade de vendas")
plt.tight_layout()
plt.show()

# ===================================
# PARTICIPAÇÃO DAS CATEGORIAS NO FATURAMENTO - PIZZA
# ===================================

faturamento_categoria.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Participação no Faturamento por Categoria")
plt.ylabel("")
plt.tight_layout()
plt.show()

# ===================================
# DISTRIBUIÇÃO E POSSÍVEIS VALORES EXTREMOS - BOXPLOT
# ===================================

df["valor_venda"].plot(kind="box")

plt.title("Distribuição do Valor das Vendas")
plt.ylabel("Valor da venda (R$)")
plt.tight_layout()
plt.show()

# ===================================
# DENSIDADE DOS VALORES DAS VENDAS - KDE
# ===================================

df["valor_venda"].plot(kind="kde")

plt.title("Densidade do valor das Vendas")
plt.xlabel("Valor da Venda (R$)")
plt.tight_layout()
plt.show()


# ===================================
# QUANTIDADE VENDIDA X VALOR DA VENDA - SCATTER , dispersão. Verificar se há relação entre os dois
# ===================================

df.plot(
    kind="scatter",
    x="quantidade",
    y="valor_venda"
)

plt.title("Quantidade Vendida X Valor da Venda")
plt.xlabel("Quantidade")
plt.ylabel("Valor de Venda (R$)")
plt.tight_layout()
plt.show()

# ===================================
# PREÇO UNITÁRIO X VALOR DA VENDA
# ===================================

df.plot(
    kind="scatter",
    x="preco_unitario",
    y="valor_venda"
)

plt.title("Preço Unitário X Valor da Venda")
plt.xlabel("Preço Unitário (R$)")
plt.ylabel("Valor da Venda(R$)")
plt.tight_layout()
plt.show()