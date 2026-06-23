from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Molecula

app = FastAPI()

@app.get("/")
def root():
    return {"message": "BraCoLi API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Adicionado :path para que o FastAPI capture barras "/" sem quebrar a rota
@app.get("/moleculas/SMILES/{smiles_string:path}")
def obter_molecula_por_smiles(smiles_string: str, db: Session = Depends(get_db)):
    molecula = db.query(Molecula).filter(Molecula.SMILES == smiles_string).first()
    
    if not molecula:
        raise HTTPException(status_code=404, detail="Molécula não encontrada no banco de dados.")
        
    return molecula