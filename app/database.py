import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

# Monta a URL de conexão usando as variáveis de ambiente
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Molecula(Base):
    __tablename__ = "moleculas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    molecular_formula = Column(String)
    molar_mass = Column(Float)  # Corresponde ao Molar Mass (g/mol)
    SMILES = Column(String, index=True)
    melting_range = Column(String) # Usando string caso tenha intervalos tipo "120-122"
    type = Column(String)
    origin = Column(String)
    observation = Column(Text)
    reference = Column(Text)

# Função utilitária para abrir/fechar sessões nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()