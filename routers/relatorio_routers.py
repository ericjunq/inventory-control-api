import pandas as pd 
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from dependencies import get_db
from security import get_current_user
from models import Usuario, Produto, Movimentacoes
from fastapi.responses import FileResponse
from enums import OrdemEnum, PeriodoEnum
from sqlalchemy import func
from datetime import datetime, timezone, timedelta

relatorio_router = APIRouter(prefix='/relatorio', tags=['relatorio'])

@relatorio_router.get('/relatorio_estoque_baixo')
async def relatorio_estoque_abaixo_min(
        exportar: bool = False,
        db: Session = Depends(get_db),
        usuario: Usuario = Depends(get_current_user)
):
    # Filtra todos os produtos que tem quantidade abaixo do estoque mínimo
    produtos = db.query(Produto).filter(Produto.usuario_id == usuario.id, Produto.quantidade < Produto.estoque_minimo).all()

    # criação de dataframe pra resposta padronizada
    produtos_df = pd.DataFrame([
            {
                'id': p.id,
                'codigo_produto': p.sku,
                'nome': p.nome, 
                'categoria': p.categoria.value,
                'quantidade': p.quantidade,
                'estoque_minimo': p.estoque_minimo
            } for p in produtos
        ])
    
    # verifica se o dicionário está vazio, já que o groupby que abaixo quebraria o codigo
    if produtos_df.empty:
        return {}
    

    resultado = produtos_df.groupby('categoria').apply( # filtra por categoria
        lambda gp: gp[['id', 'codigo_produto', 'nome', 'quantidade', 'estoque_minimo']].to_dict('records') # converte o dataframe de cada grupo em um dicionario
    ).to_dict() # transforma o objeto pandas em um dicionário python

    # cria um arquivo Excel com a tabela dos produtos abaixo do estoque mínimo
    if exportar:
        produtos_df.to_excel('relatorio_estoque_baixo.xlsx', index=False)
        return FileResponse(
            'relatorio_estoque_baixo.xlsx',
            filename='relatorio_estoque_baixo.xlsx',
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    # retorna os produtos abaixo do estoque mínimo
    return resultado


@relatorio_router.get('/ordenar_produtos_movimentados')
async def ordenar_produtos(
    exportar: bool = False,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
    ordem: OrdemEnum = OrdemEnum.mais_movimentados
):
    
    produtos = db.query(
        # colunas do banco
        Produto.id,
        Produto.nome,
        Produto.sku,
        Produto.categoria, 
        func.sum(Movimentacoes.quantidade).label('total_movimentado')  # soma todas as movimentações do produto e chama de 'total_movimentado'
    ).join(
        Movimentacoes, Movimentacoes.produto_id == Produto.id  # une as tabelas onde o produto_id da movimentação bate com o id do produto
    ).filter(
        Produto.usuario_id == usuario.id  # garante que só traz produtos do usuário logado
    ).group_by(
        Produto.id  # agrupa por produto pra o SUM funcionar corretamente, sem isso ele somaria tudo junto
    ).all()  # executa a query e retorna todos os resultados

    # criação de dataframe pra resposta padronizada
    produtos_df = pd.DataFrame([
        {
            'id': p.id,
            'codigo_produto': p.sku,
            'nome': p.nome, 
            'categoria': p.categoria.value,
            'total_movimentacoes' : p.total_movimentado
        } for p in produtos
    ])

    if produtos_df.empty:
        return {}
    
    # Verifica a ordem de filtro de movimentações recebida (crescente ou decrescente)
    if ordem == OrdemEnum.mais_movimentados:
        crescente = False
    if ordem == OrdemEnum.menos_movimentados:
        crescente = True

    # organiza de acordo a ordem
    produtos_df = produtos_df.sort_values(ascending=crescente)

    # cria arquivo no Excel da tabela dos produtos ordenando baseado filtro escolhido das suas movimentações
    if exportar:
        produtos_df.to_excel('relatorio_ordenado.xlsx', index=False)
        return FileResponse(
            'relatorio_ordenado.xlsx',
            filename='relatorio_ordenado.xlsx',
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    # retorna os produtos ordenados de acordo o filtro das suas movimentações
    return produtos_df.to_dict('records')


@relatorio_router.get('/ordenar_periodo')
async def ordenar_periodo(
    exportar: bool = False,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
    periodo: PeriodoEnum = PeriodoEnum.mes
):  
    agora = datetime.now(timezone.utc)
    if periodo == PeriodoEnum.dia:
        data_inicial = agora - timedelta(days=1)
    elif periodo == PeriodoEnum.semana:
        data_inicial = agora - timedelta(weeks=1)
    elif periodo == PeriodoEnum.mes:
        data_inicial = agora - timedelta(days=30)
    elif periodo == PeriodoEnum.trimestre:
        data_inicial = agora - timedelta(days=90)
    elif periodo == PeriodoEnum.semestre:
        data_inicial = agora - timedelta(days=180)
    elif periodo == PeriodoEnum.ano:
        data_inicial = agora - timedelta(days=365)
    
    produtos = db.query(
        # Colunas do banco
        Produto.id,
        Produto.sku,
        Produto.nome,
        Produto.categoria,
        Movimentacoes.tipo,
        Movimentacoes.quantidade,
        Movimentacoes.observacao,
        Movimentacoes.created_at
    ).join(
        Produto, Produto.id == Movimentacoes.produto_id # União de tabelas 
    ).filter(
        Produto.usuario_id == usuario.id, # verifica que cada usuario tem acesso aos próprios produtos
        Movimentacoes.created_at >= data_inicial # filtra periodo selecionado
    ).all()

    # criação de dataframe pra resposta padronizada
    produtos_df = pd.DataFrame([
        {
            'id': p.id,
            'codigo_produto': p.sku,
            'nome': p.nome,
            'categoria': p.categoria.value,
            'movimentacao': p.tipo.value,
            'quantidade': p.quantidade,
            'criado_em': p.created_at
        } for p in produtos
    ])

    # verifica se o dicionário ta vazio
    if produtos_df.empty:
        return {}
    
    # alteração do nome de arquivo (desnecessário, só por que eu quis)
    if exportar:
        produtos_df.to_excel(f'relatorio_{periodo.value}.xlsx')
        return FileResponse(
            f'relatorio_{periodo.value}.xlsx',
            filename=f'relatorio_{periodo.value}.xlsx',
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    return produtos_df.to_dict('records')