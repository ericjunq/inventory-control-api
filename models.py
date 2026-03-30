from sqlalchemy import Column, String, DateTime, Integer, Boolean, Float, func, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from database import Base
import uuid
from enums import CategoriasEnum, MovimentacoesEnum

# Cria tabela de Usuários no banco
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String(30), nullable=False)
    sobrenome = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, unique=True)
    senha_hash = Column(String, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    telefone = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(Boolean, default=True)

    produtos = relationship('Produto', back_populates='usuario')

# Cria a tabela de Produtos no banco
class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria = Column(SAEnum(CategoriasEnum), nullable=False)
    nome = Column(String(40), nullable=False)
    descricao = Column(String(50))
    sku = Column(String, nullable=False, unique=True, default= lambda: str(uuid.uuid4())[:8].upper())
    preco_produto = Column(Float, nullable=False)
    preco_venda = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    estoque_minimo = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship('Usuario', back_populates='produtos')

    movimentacoes = relationship('Movimentacoes', back_populates='produto')

# Cria a tabela de movimentações (entrada e saida de produtos)

class Movimentacoes(Base):
    __tablename__ = 'compra_venda'

    id = Column(Integer, autoincrement=True, primary_key=True)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    tipo = Column(SAEnum(MovimentacoesEnum), nullable=False)
    quantidade = Column(Integer, nullable=False)
    observacao = Column(String(60))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    produto = relationship('Produto', back_populates='movimentacoes')

