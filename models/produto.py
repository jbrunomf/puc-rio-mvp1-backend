from datetime import datetime
from typing import Optional

from models.base import Base
import sqlalchemy.orm as so
import sqlalchemy as sa


class Produto(Base):
    __tablename__ = 'produto'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    descricao: so.Mapped[str] = so.mapped_column(sa.String(120))
    preco_custo: so.Mapped[float] = so.mapped_column(sa.Float)
    preco_venda: so.Mapped[float] = so.mapped_column(sa.Float)
    data_criacao: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)
    is_novo: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    imagem: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=True)

    def to_dict(self):
        return {"id": self.id, "descricao": self.descricao, "preco_custo": self.preco_custo,
                "preco_venda": self.preco_venda, "data_criacao": self.data_criacao, "is_novo": self.is_novo}

    def __repr__(self):
        return (f"Produto(id={self.id}, descricao='{self.descricao}', "
                f"preco_custo={self.preco_custo}, preco_venda={self.preco_venda})")
