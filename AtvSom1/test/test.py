import pytest
import pytest_asyncio
import sys
import os
from httpx import AsyncClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app, estudantes_db, next_id

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    estudantes_db.clear()
    global next_id
    next_id = 1
    yield
    estudantes_db.clear()
    global next_id
    next_id = 1

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_criar_estudante(client):
    estudante_data = {
        "nome": "João Silva",
        "idade": 20,
        "curso": "Ciência da Computação",
        "matricula": "2024001"
    }
    
    response = await client.post("/estudantes", json=estudante_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "João Silva"
    assert data["id"] == 1

@pytest.mark.asyncio
async def test_listar_estudantes(client):
    estudante = {"nome": "Maria", "idade": 22, "curso": "SI", "matricula": "002"}
    await client.post("/estudantes", json=estudante)
    
    response = await client.get("/estudantes")
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nome"] == "Maria"

@pytest.mark.asyncio
async def test_buscar_estudante_por_id(client):
    estudante_data = {"nome": "Pedro", "idade": 21, "curso": "ADS", "matricula": "003"}
    create_response = await client.post("/estudantes", json=estudante_data)
    estudante_id = create_response.json()["id"]
    
    response = await client.get(f"/estudantes/{estudante_id}")
    
    assert response.status_code == 200
    assert response.json()["nome"] == "Pedro"

@pytest.mark.asyncio
async def test_atualizar_estudante(client):
    estudante_data = {"nome": "Ana", "idade": 19, "curso": "CC", "matricula": "004"}
    create_response = await client.post("/estudantes", json=estudante_data)
    estudante_id = create_response.json()["id"]
    
    dados_atualizados = {"nome": "Ana Silva", "idade": 20, "curso": "CC", "matricula": "004"}
    response = await client.put(f"/estudantes/{estudante_id}", json=dados_atualizados)
    
    assert response.status_code == 200
    assert response.json()["nome"] == "Ana Silva"

@pytest.mark.asyncio
async def test_deletar_estudante(client):
    estudante_data = {"nome": "Carlos", "idade": 23, "curso": "SI", "matricula": "005"}
    create_response = await client.post("/estudantes", json=estudante_data)
    estudante_id = create_response.json()["id"]
    
    response = await client.delete(f"/estudantes/{estudante_id}")
    
    assert response.status_code == 200
    assert len(estudantes_db) == 0
