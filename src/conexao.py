from sqlalchemy import create_engine


USUARIO = "postgres"
SENHA = "1234"
HOST = "localhost"
PORTA = "5432"
BANCO = "analise_vendas"


url = f"postgresql+psycopg2://postgres:1234@localhost:5432/analise_vendas"

engine = create_engine(url)

with engine.connect() as conexao:
 print("Conexão em PostgreSQL realizada com sucesso")