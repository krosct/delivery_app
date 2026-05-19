from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from modulos.cardapio.controle import CardapioControle

router = APIRouter(tags=["Cardápio"])

# ── Schemas ───────────────────────────────────────────────────────────────────

class ItemCreate(BaseModel):
    nome: str
    preco: float
    descricao: Optional[str] = None

class ItemUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    descricao: Optional[str] = None

class CategoriaCreate(BaseModel):
    nome: str

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None

class AssociarCategoria(BaseModel):
    id_categoria: int

# ── Rotas de itens ────────────────────────────────────────────────────────────

@router.post("/restaurantes/{restaurante_id}/items", status_code=201)
async def cadastrar_item(restaurante_id: int, item: ItemCreate):
    resultado = CardapioControle.cadastrar_item(restaurante_id, item.model_dump())
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.get("/restaurantes/{restaurante_id}/items", status_code=200)
async def listar_itens(restaurante_id: int):
    resultado = CardapioControle.listar_itens(restaurante_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado["itens"]

@router.get("/restaurantes/{restaurante_id}/items/{item_id}", status_code=200)
async def buscar_item(restaurante_id: int, item_id: int):
    resultado = CardapioControle.buscar_item(restaurante_id, item_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado["item"]

@router.put("/restaurantes/{restaurante_id}/items/{item_id}", status_code=200)
async def atualizar_item(restaurante_id: int, item_id: int, dados: ItemUpdate):
    dados_atualizacao = {k: v for k, v in dados.model_dump().items() if v is not None}
    resultado = CardapioControle.atualizar_item(restaurante_id, item_id, dados_atualizacao)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.delete("/restaurantes/{restaurante_id}/items/{item_id}", status_code=200)
async def remover_item(restaurante_id: int, item_id: int):
    resultado = CardapioControle.remover_item(restaurante_id, item_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

# ── Rotas de categorias ───────────────────────────────────────────────────────

@router.post("/restaurantes/{restaurante_id}/categories", status_code=201)
async def cadastrar_categoria(restaurante_id: int, categoria: CategoriaCreate):
    resultado = CardapioControle.cadastrar_categoria(restaurante_id, categoria.model_dump())
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.get("/restaurantes/{restaurante_id}/categories", status_code=200)
async def listar_categorias(restaurante_id: int):
    resultado = CardapioControle.listar_categorias(restaurante_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado["categorias"]

@router.put("/restaurantes/{restaurante_id}/categories/{categoria_id}", status_code=200)
async def atualizar_categoria(restaurante_id: int, categoria_id: int, dados: CategoriaUpdate):
    dados_atualizacao = {k: v for k, v in dados.model_dump().items() if v is not None}
    resultado = CardapioControle.atualizar_categoria(restaurante_id, categoria_id, dados_atualizacao)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.delete("/restaurantes/{restaurante_id}/categories/{categoria_id}", status_code=200)
async def remover_categoria(restaurante_id: int, categoria_id: int):
    resultado = CardapioControle.remover_categoria(restaurante_id, categoria_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.patch("/restaurantes/{restaurante_id}/items/{item_id}/category", status_code=200)
async def associar_categoria(restaurante_id: int, item_id: int, corpo: AssociarCategoria):
    resultado = CardapioControle.associar_categoria(restaurante_id, item_id, corpo.id_categoria)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

# ── Rotas de cardápio público ─────────────────────────────────────────────────

@router.post("/restaurantes/{restaurante_id}/menu/share", status_code=200)
async def gerar_link_publico(restaurante_id: int):
    resultado = CardapioControle.gerar_link_publico(restaurante_id)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado

@router.get("/menu/{slug}", status_code=200)
async def cardapio_publico(slug: str):
    resultado = CardapioControle.cardapio_publico(slug)
    if "erro" in resultado:
        raise HTTPException(status_code=resultado["status_code"], detail=resultado["erro"])
    return resultado