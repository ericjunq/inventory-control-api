from enum import Enum

class CategoriasEnum(str, Enum):
    eletronicos = "Eletronicos"
    roupas = "Roupas"
    calcados = "Calcados"
    alimentos = "Alimentos"
    beleza = "Beleza e Cuidados"
    esportes = "Esportes"
    moveis = "Moveis"
    livros = "Livros"
    brinquedos = "Brinquedos"
    outros = "Outros"

class MovimentacoesEnum(str, Enum):
    saida = 'saida'
    entrada = 'entrada'

class MotivoAjusteEnum(str, Enum):
    correcao_estoque = "Correção de estoque"
    perda = "Perda/Avaria"
    devolucao = "Devolução"
    inventario = "Inventário físico"
    outros = "Outros"

class OrdemEnum(str, Enum):
    mais_movimentados = "mais_movimentados"
    menos_movimentados = "menos_movimentados"

class PeriodoEnum(str, Enum):
    dia = 'dia'
    semana = 'semana'
    mes = 'mes'
    trimestre = 'trimestre'
    semestre = 'semestre'
    ano = 'ano'