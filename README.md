📦 Inventory Control API
API REST para controle de estoque com análise de dados integrada, desenvolvida com FastAPI, SQLAlchemy e Pandas.
🚀 Tecnologias

FastAPI — framework web moderno e de alta performance
SQLAlchemy — ORM para comunicação com o banco de dados
SQLite — banco de dados (migração para PostgreSQL planejada)
Pandas — análise e exportação de dados
Pydantic — validação de dados e schemas
JWT — autenticação via tokens
pwdlib — criptografia de senhas


📁 Estrutura do Projeto
inventory-control-api/
├── main.py                    # Inicialização da aplicação
├── database.py                # Configuração do banco de dados
├── models.py                  # Modelos das tabelas
├── schemas.py                 # Schemas Pydantic
├── dependencies.py            # Dependências (sessão do banco)
├── security.py                # JWT e criptografia
├── validations.py             # Validações de CPF e telefone
├── enums.py                   # Enums do projeto
├── requirements.txt           # Dependências do projeto
├── .env.example               # Exemplo de variáveis de ambiente
└── routers/
    ├── auth_routers.py        # Rotas de autenticação
    ├── produtos_routers.py    # Rotas de produtos
    ├── movimentacoes_routers.py # Rotas de movimentações
    └── relatorios_routers.py  # Rotas de relatórios (Pandas)

⚙️ Como Rodar o Projeto
Pré-requisitos

Python 3.13+
Git

1. Clone o repositório
bashgit clone https://github.com/ericjunq/inventory-control-api.git
cd inventory-control-api
2. Crie e ative a venv
bashpython -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
3. Instale as dependências
bashpip install -r requirements.txt
4. Configure as variáveis de ambiente
bashcp .env.example .env
Edite o .env com suas configurações:
envDATABASE_URL=sqlite:///./estoque.db
SECRET_KEY=sua_chave_secreta
ACCESS_TOKEN_EXPIRES_MINUTES=30
REFRESH_TOKEN_EXPIRES_DAYS=7
ALGORITHM=HS256
5. Rode a aplicação
bashuvicorn main:app --reload
Acesse a documentação em: http://127.0.0.1:8000/docs

🔐 Autenticação
A API utiliza JWT para autenticação. Para acessar as rotas protegidas:

Cadastre um usuário em POST /users/cadastro
Faça login em POST /users/login
Use o access_token retornado no header Authorization: Bearer <token>


📌 Rotas
Usuários
MétodoRotaDescriçãoPOST/users/cadastroCadastro de usuárioPOST/users/loginLogin e geração de tokensPATCH/users/editar_usuarioEdição de dados do usuário
Produtos
MétodoRotaDescriçãoPOST/produtos/cadastrar_produtoCadastro de produtoGET/produtos/listar_produtosListagem com filtros (id, nome, sku, categoria)PATCH/produtos/editar_produto/{produto_id}Edição de produto
Movimentações
MétodoRotaDescriçãoPOST/movimentacoes/movimentar_estoque/{produto_id}Registra entrada ou saída de estoque
Relatórios (Pandas)
MétodoRotaDescriçãoGET/relatorios/relatorio_estoque_baixoProdutos abaixo do estoque mínimoGET/relatorios/ordenar_produtos_movimentadosRanking de produtos mais/menos movimentadosGET/relatorios/ordenar_periodoMovimentações por período (dia, semana, mês, trimestre, semestre, ano)

Todos os relatórios aceitam o parâmetro ?exportar=true para download em Excel (.xlsx)


📊 Funcionalidades com Pandas

Agrupamento por categoria — produtos organizados por categoria na listagem
Alerta de estoque baixo — aviso automático quando a quantidade atinge o mínimo
Ranking de movimentações — ordenação por produtos mais ou menos movimentados
Relatórios por período — análise de entradas e saídas com filtro temporal
Exportação em Excel — todos os relatórios podem ser exportados em .xlsx


🔒 Segurança

Senhas criptografadas com pwdlib
Autenticação via JWT com access e refresh token
Validação de CPF com algoritmo oficial
Validação de telefone via regex
Cada usuário acessa apenas os próprios produtos


🗄️ Modelos do Banco
Usuario
CampoTipoDescriçãoidIntegerChave primárianomeStringNome do usuáriosobrenomeStringSobrenomeemailStringEmail únicocpfStringCPF únicotelefoneStringTelefone únicostatusBooleanAtivo/Inativo
Produto
CampoTipoDescriçãoidIntegerChave primáriaskuStringCódigo único gerado automaticamentenomeStringNome padronizado (casefold)categoriaEnumCategoria do produtopreco_produtoFloatPreço de custopreco_vendaFloatPreço de vendaquantidadeIntegerQuantidade em estoqueestoque_minimoIntegerLimite mínimo para alerta
Movimentacao
CampoTipoDescriçãoidIntegerChave primáriaproduto_idIntegerFK para ProdutotipoEnumentrada ou saidaquantidadeIntegerQuantidade movimentadaobservacaoStringContexto da movimentação

👨‍💻 Autor
Eric — github.com/ericjunq
