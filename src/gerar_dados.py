import pandas as pd
import numpy as np

np.random.seed(42)

quantidade_registros = 5000

produtos = [
    "Notebook",
    "Monitor",
    "Teclado",
    "Mouse",
    "Headset",
    "Celular",
    "Tablet",
    "Cadeira",
    "Mesa",
    "Impressora"
] 

categorias = {
    "Notebook": "Eletrônicos",
    "Monitor": "Eletrônicos",
    "Teclado": "Periféricos",
    "Mouse": "Periféricos",
    "Headset": "Periféticos",
    "Celular": "Eletrônicos",
    "Tablet": "Eletrônicos",
    "Cadeira": "Móveis",
    "Mesa": "Móveis",
    "Impressora": "Eletrônicos"
}

regioes = [
    "Sul",
    "Sudeste",
    "Centro-Oeste",
    "Nordeste",
    "Norte"
]

formas_pagamento = [
    "Cartão de crédito",
    "Cartão de débito",
    "Pix",
    "Boleto",
]

datas = pd.to_datetime(
    np.random.randint(
        pd.Timestamp("2025-01-01").value // 10**9,
        pd.Timestamp("2025-12-31 23:59:59").value //10**9,
        quantidade_registros
    ),
    unit="s"
)

df = pd.DataFrame({
    "data": datas,
    "pedido": np.arange(10001, 10001 + quantidade_registros),
    "cliente": np.random.randint(1, 1001, quantidade_registros),
    "produto": np.random.choice(produtos, quantidade_registros),
    "regiao": np.random.choice(regioes, quantidade_registros),
    "quantidade": np.random.randint(1, 6, quantidade_registros),
    "forma_pagamento": np.random.choice(formas_pagamento, quantidade_registros),
})

precos = {
    "Notebook": 3500,
    "Monitor": 1200,
    "Teclado": 250,
    "Mouse": 120,
    "Headset": 300,
    "Celular": 2200,
    "Tablet": 1500,
    "Cadeira": 850,
    "Mesa": 1100,
    "Impressora": 900,
}

df["preco_unitario"] = df["produto"].map(precos)

df["desconto"] = np.round(
    np.random.uniform(0, 0.15, quantidade_registros),
    2
)

df["valor_bruto"] = (
    df["quantidade"] * df["preco_unitario"]
)

df["valor_desconto"] = (
    df["valor_bruto"] * df["desconto"]
)

df["valor_venda"] = (
    df["valor_bruto"] - df["valor_desconto"]
).round(2)

df["categoria"] = df["produto"].map(categorias)

df.to_csv(
    "dados/vendas.csv",
    index=False
)

print("Dataset criado com sucesso!")
print(f"Quantidade de registro: {len(df)}")
print("\nPrimeiros registros:")
print(df.head())