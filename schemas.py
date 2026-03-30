from pydantic import BaseModel, EmailStr
from typing import Optional
from enums import CategoriasEnum, MotivoAjusteEnum, MovimentacoesEnum
from datetime import datetime

# Usuarios
class UsuarioSchema(BaseModel):
    nome: str 
    sobrenome: str 
    email: EmailStr
    senha: str 
    cpf: str 
    telefone: str 

class UsuarioCreateResponse(BaseModel):
    nome:str 
    sobrenome:str 
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    telefone: Optional[str] = None

class UsuarioUpdateResponse(BaseModel):
    nome:str 
    sobrenome:str 
    email: EmailStr
    updated_at: datetime

    class Config:
        from_attributes = True


# Produtos
class ProdutoSchema(BaseModel):
    categoria: CategoriasEnum
    nome: str 
    descricao: Optional[str] = None 
    preco_produto: float 
    preco_venda: float 
    quantidade: int 
    estoque_minimo: int 

class ProdutoResponse(BaseModel):
    categoria: CategoriasEnum
    nome: str 
    descricao: Optional[str] = None 
    preco_produto: float 
    preco_venda: float 
    quantidade: int 
    estoque_minimo: int 
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProdutoUpdate(BaseModel):
    descricao: Optional[str] = None 
    preco_produto: Optional[float] = None
    preco_venda: Optional[float] = None
    quantidade: Optional[int] = None
    estoque_minimo: Optional[int] = None
    motivo_update: Optional[MotivoAjusteEnum] = None

class ProdutoUpdateResponse(BaseModel):
    categoria: CategoriasEnum
    nome: str 
    descricao: Optional[str] = None 
    preco_produto: float 
    preco_venda: float 
    quantidade: int 
    estoque_minimo: int 
    updated_at: datetime

    class Config:
        from_attributes = True


# Movimentações 
class MovimentacoesSchema(BaseModel):
    tipo: MovimentacoesEnum
    quantidade: int 
    observacao: Optional[str] = None 

class MovimentacoesResponse(BaseModel):
    id: int
    produto_id: int 
    tipo: MovimentacoesEnum
    quantidade: int 
    observacao: Optional[str] = None
    created_at: datetime

class MovimentacoesComAviso(BaseModel):
    movimentacao: MovimentacoesResponse
    aviso: str 

    class Config:
        from_attributes = True
