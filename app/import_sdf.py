import os
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
from app.database import get_db, Composto

def processar_sdf():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_sdf = os.path.join(BASE_DIR, "BraCoLi_v1.sdf")

    db = next(get_db())  # Obtém uma sessão do banco de dados

    try:
        # Chem.SDMolSupplier lê arquivos .sdf linha por linha
        with open(caminho_sdf, 'rb') as f:
            supplier = Chem.ForwardSDMolSupplier(f)

            # Contador para simular ou gerar o ID incremental BraCoLi (ex: BR010001, BR010002...)
            contador_id = 10001 

            for mol in supplier:
                if mol is None:
                    # RDKit retorna None se houver algum erro de estrutura na molécula do arquivo
                    continue
                
                # 1. Gerar o ID BraCoLi formatado
                bracoli_id = f"BR0{contador_id}"
                
                # 2. Gerar SMILES (representação textual da estrutura química)
                smiles = Chem.MolToSmiles(mol)
                
                # 3. Gerar InChI (Identificador Químico Internacional IUPAC)
                inchi = Chem.MolToInchi(mol)
                
                # 4. Gerar InChIKey (Versão hash compactada do InChI de 27 caracteres estável)
                inchikey = Chem.InchiToInchiKey(inchi)
                
                # 5. Gerar Peso Molecular (molecular_weight)
                peso_molecular = Descriptors.MolWt(mol)
                
                # 6. Gerar Fingerprint (usado para buscas por similaridade química)
                fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
                # Para salvar no banco, o fingerprint é convertido em uma string hexadecimal
                fp_hex = fingerprint.ToBitString()

                novo_composto = Composto(
                    id=bracoli_id,
                    smiles=smiles,
                    inchikey=inchikey,
                    molecular_weight=peso_molecular,
                    fingerprint=fp_hex
                )

                db.add(novo_composto)  # Adiciona o novo composto à sessão do banco de dados
                
                contador_id += 1
        
        db.commit()  # Salva todas as alterações no banco de dados

    except Exception as e:
        db.rollback()  # Reverte qualquer alteração em caso de erro
        print(f"Erro ao processar o arquivo SDF: {e}")

    finally:
        db.close()  # Fecha a sessão do banco de dados    

if __name__ == "__main__":
    processar_sdf()
