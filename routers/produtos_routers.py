from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from security import get_current_user
from models import Usuario, Produto, Movimentacoes
from schemas import ProdutoResponse, ProdutoSchema, ProdutoUpdate, ProdutoUpdateResponse
import pandas as pd
from enums import CategoriasEnum

produtos_router = APIRouter(prefix='/produtos', tags=['produtos'])

# Cadastro de produto
@produtos_router.post('/cadastrar_produto', response_model=ProdutoResponse)
async def cadastrar_produto(
    produtoschema: ProdutoSchema, 
    db: Session = Depends(get_db), 
    usuario: Usuario = Depends(get_current_user)
):
    # padroniza o nome do produto pra garantir que não tenha duplicação de produtos no banco
    nome_produto = produtoschema.nome.strip().casefold()

    # verifica se ja existe produto com aquele nome
    produto_existente = db.query(Produto).filter(Produto.nome == nome_produto).first()
    if produto_existente:
        raise HTTPException(status_code=409, detail='Produto já cadastrado')
    
    # cria o produto
    produto = Produto(
        categoria = produtoschema.categoria,
        nome = nome_produto,
        descricao = produtoschema.descricao,
        preco_produto = produtoschema.preco_produto,
        preco_venda = produtoschema.preco_venda,
        quantidade = produtoschema.quantidade,
        estoque_minimo = produtoschema.estoque_minimo,
        usuario_id = usuario.id
    )

    # Insere o produto no banco
    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto

@produtos_router.get('/listar_produtos')
async def listar_produtos(
    categoria: CategoriasEnum = None,
    id: int = None, 
    nome: str = None, 
    sku: str = None, 
    db: Session = Depends(get_db), 
    usuario: Usuario = Depends(get_current_user)
):
    
    query = db.query(Produto).filter(Produto.usuario_id == usuario.id)

    # filtro por categoria
    if categoria:
        query = query.filter(Produto.categoria == categoria)
    
    # filtro por id
    if id:
        query = query.filter(Produto.id == id)
    
    # filtro por nome
    if nome:
        nome_padronizado = nome.replace(' ','').casefold().strip()
        query = query.filter(Produto.nome.ilike(f'%{nome_padronizado}%'))
    
    # filtro por sku
    if sku:
        query = query.filter(Produto.sku == sku)
    
    produtos = query.all()

    # criação de dataframe pra resposta padronizada

    produtos_df = pd.DataFrame(
        [
            {
                'categoria': p.categoria.value,
                'nome': p.nome,
                'codigo_produto': p.sku,
                'quantidade': p.quantidade
            } for p in produtos
        ]
    )

    # verifica se o dicionário está vazio, já que o groupby que abaixo quebraria o codigo
    if produtos_df.empty:
        return {}

    resultado = produtos_df.groupby('categoria').apply( # filtra por categoria
        lambda gp: gp[['nome','codigo_produto','quantidade']].to_dict('records') # converte o dataframe de cada grupo em um dicionario
        ).to_dict() # transforma o objeto pandas em um dicionário python
    
    return resultado


# Rota para editar produto 
@produtos_router.patch('/editar_produto/{produto_id}', response_model=ProdutoUpdateResponse)
async def editar_produto(
    produto_id: int,
    produto_update: ProdutoUpdate, 
    db: Session = Depends(get_db), 
    usuario: Usuario = Depends(get_current_user)
):
    # verifica se o produto existe e garante que o usuário edite apenas os próprios produtos
    produto = db.query(Produto).filter(Produto.id == produto_id, Produto.usuario_id == usuario.id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    
    # transforma os dados recebidos em formato de dicionário
    dados_update = produto_update.dict(exclude_unset=True)

    # Verificação: Caso a quantidade do produto seja alterada, deve ser justificada (devolução, perda, correção etc)
    if dados_update.get('quantidade') and not dados_update.get('motivo_update'):
        raise HTTPException(status_code=400, detail='Informe o motivo da alteração do estoque')

    for campo, valor in dados_update.items():
        setattr(produto, campo, valor) 

    db.commit()
    db.refresh(produto)
    
    return produto 