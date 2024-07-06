from datetime import datetime
from typing import List
from pydantic import BaseModel
from typing_extensions import Optional


class ProdutoSchema(BaseModel):
    descricao: str
    preco_custo: float
    preco_venda: float
    data_criacao: Optional[datetime] = None
    is_novo: bool
    imagem: Optional[str] = None


class ProdutoListSchema(BaseModel):
    produtos: List[ProdutoSchema]


class DeleteProdutoSchema(BaseModel):
    id: int
    message: str


class ProdutoQuerySchema(BaseModel):
    id: int
