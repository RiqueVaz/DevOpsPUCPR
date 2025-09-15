import random
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="API de Estudantes", version="1.0.0")


class Estudante(BaseModel):
    id: Optional[int] = None
    nome: str
    idade: int
    curso: str
    matricula: str


estudantes_db: List[Estudante] = []
next_id = 1


@app.post("/estudantes", response_model=Estudante)
async def criar_estudante(estudante: Estudante):
    global next_id
    estudante.id = next_id
    next_id += 1
    estudantes_db.append(estudante)
    return estudante


@app.get("/estudantes", response_model=List[Estudante])
async def listar_estudantes():
    return estudantes_db

@app.get("/estudantes/{estudante_id}", response_model=Estudante)
async def buscar_estudante(estudante_id: int):
    for estudante in estudantes_db:
        if estudante.id == estudante_id:
            return estudante
    raise HTTPException(status_code=404, detail="Estudante não encontrado")


@app.put("/estudantes/{estudante_id}", response_model=Estudante)
async def atualizar_estudante(estudante_id: int, estudante_atualizado: Estudante):
    for i, estudante in enumerate(estudantes_db):
        if estudante.id == estudante_id:
            estudante_atualizado.id = estudante_id
            estudantes_db[i] = estudante_atualizado
            return estudante_atualizado
    raise HTTPException(status_code=404, detail="Estudante não encontrado")


@app.delete("/estudantes/{estudante_id}")
async def deletar_estudante(estudante_id: int):
    for i, estudante in enumerate(estudantes_db):
        if estudante.id == estudante_id:
            estudantes_db.pop(i)
            return {"message": "Estudante deletado com sucesso"}
    raise HTTPException(status_code=404, detail="Estudante não encontrado")