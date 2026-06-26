from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, Molecula, Composto

app = FastAPI()

@app.get("/")
def root():
    return {"message": "BraCoLi API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/moleculas/smiles/{smiles_string:path}")
def obter_molecula_por_smiles(smiles_string: str, db: Session = Depends(get_db)):
    molecula = db.query(Molecula).filter(Molecula.smiles == smiles_string).first()
    
    if not molecula:
        raise HTTPException(status_code=404, detail="Molécula não encontrada no banco de dados.")
        
    return molecula

@app.get("/compounds/{compound_id:path}")
def obter_composto_por_id(compound_id: str, db: Session = Depends(get_db)):
    composto = db.query(Composto).filter(Composto.id == compound_id).first()
    
    if not composto:
        raise HTTPException(status_code=404, detail="Composto não encontrado no banco de dados.")
        
    return composto
