from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session 
from schemas import MovimentacoesSchema, MovimentacoesResponse, MovimentacoesComAviso
from models import Movimentacoes, Usuario, Produto
from dependencies import get_db
from security import get_current_user
from enums import MovimentacoesEnum
from typing import Union

movimentacoes_router = APIRouter()

@movimentacoes_router.post('/movimentar_estoque/{produto_id}', response_model=Union[MovimentacoesResponse, MovimentacoesComAviso])
async def movimentar_estoque(
    produto_id: int,
    movimentacaoschema: MovimentacoesSchema,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user)
):
    # verifica se o produto existe e garante que o usuário só pode editar o próprio produto
    produto = db.query(Produto).filter(Produto.id == produto_id, Produto.usuario_id == usuario.id). first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    
    # adiciona a quantidade no estoque atual
    if movimentacaoschema.tipo == MovimentacoesEnum.entrada:
        produto.quantidade += movimentacaoschema.quantidade
    
    # diminui a quantidade do estoque atual
    elif movimentacaoschema.tipo == MovimentacoesEnum.saida:
        # garante que a quantidade retirada do estoque não seja maior do que a quantidade atual do estoque
        if produto.quantidade < movimentacaoschema.quantidade:
            raise HTTPException(status_code=400, detail='Quantidade insuficiente no estoque')
        
        produto.quantidade -= movimentacaoschema.quantidade
        
    # Cria a movimentação
    movimentacao = Movimentacoes(
        produto_id = produto_id,
        tipo = movimentacaoschema.tipo,
        quantidade = movimentacaoschema.quantidade,
        observacao = movimentacaoschema.observacao
    )

    # Registra a movimentação no banco
    db.add(movimentacao)
    db.commit()
    db.refresh(movimentacao)

    # Caso a quantidade de produto que tiver no estoque depois da movimentação seja menor do que a quantidade mínima do estoque é adicionada uma mensagem no retorno
    if produto.quantidade < produto.estoque_minimo:
        return MovimentacoesComAviso(movimentacao=movimentacao, aviso=f'Estoque baixo! Restam apenas {produto.quantidade} unidades de {produto.nome}. Nível mínimo de estoque: {produto.estoque_minimo} unidades')
    
    return movimentacao