import pandas as pd
from app.database import engine

# lê o excel
df = pd.read_excel("BraCoLi_v1_database.xlsx")

# padroniza colunas (IMPORTANTE)
df.columns = [
    "name",
    "molecular_formula",
    "molar_mass",
    "SMILES",
    "melting_range",
    "type",
    "origin",
    "observation",
    "reference"
]

# garante tipo correto (evita erro no REAL)
df["molar_mass"] = pd.to_numeric(df["molar_mass"], errors="coerce")

# manda pro banco
df.to_sql(
    "moleculas",
    engine,
    if_exists="append",
    index=False
)

print("Importação concluída com sucesso!")