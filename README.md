# 📦 Inventory Control API

API REST para controle de estoque com análise de dados integrada, desenvolvida com **FastAPI**, **SQLAlchemy** e **Pandas**.

## 🚀 Tecnologias

- **[FastAPI](https://fastapi.tiangolo.com/)** — framework web moderno e de alta performance
- **[SQLAlchemy](https://www.sqlalchemy.org/)** — ORM para comunicação com o banco de dados
- **[SQLite](https://www.sqlite.org/)** — banco de dados (migração para PostgreSQL planejada)
- **[Pandas](https://pandas.pydata.org/)** — análise e exportação de dados
- **[Pydantic](https://docs.pydantic.dev/)** — validação de dados e schemas
- **[JWT](https://jwt.io/)** — autenticação via tokens
- **[pwdlib](https://frankie567.github.io/pwdlib/)** — criptografia de senhas

---

## 📁 Estrutura do Projeto

```
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
```

---

## ⚙️ Como Rodar o Projeto

### Pré-requisitos
- Python 3.13+
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/ericjunq/inventory-control-api.git
cd inventory-control-api
```

### 2. Crie e ative a venv
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

Edite o `.env` com suas configurações:
```env
DATABASE_URL=sqlite:///./estoque.db
SECRET_KEY=sua_chave_secreta
ACCESS_TOKEN_EXPIRES_MINUTES=30
REFRESH_TOKEN_EXPIRES_DAYS=7
ALGORITHM=HS256
```

### 5. Rode a aplicação
```bash
uvicorn main:app --reload
```

Acesse a documentação em: **http://127.0.0.1:8000/docs**

---

## 🔐 Autenticação

A API utiliza **JWT** para autenticação. Para acessar as rotas protegidas:

1. Cadastre um usuário em `POST /users/cadastro`
2. Faça login em `POST /users/login`
3. Use o `access_token` retornado no header `Authorization: Bearer <token>`

---

## 📌 Rotas

### Usuários
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/users/cadastro` | Cadastro de usuário |
| POST | `/users/login` | Login e geração de tokens |
| PATCH | `/users/editar_usuario` | Edição de dados do usuário |

### Produtos
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/produtos/cadastrar_produto` | Cadastro de produto |
| GET | `/produtos/listar_produtos` | Listagem com filtros (id, nome, sku, categoria) |
| PATCH | `/produtos/editar_produto/{produto_id}` | Edição de produto |

### Movimentações
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/movimentacoes/movimentar_estoque/{produto_id}` | Registra entrada ou saída de estoque |

### Relatórios (Pandas)
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/relatorios/relatorio_estoque_baixo` | Produtos abaixo do estoque mínimo |
| GET | `/relatorios/ordenar_produtos_movimentados` | Ranking de produtos mais/menos movimentados |
| GET | `/relatorios/ordenar_periodo` | Movimentações por período (dia, semana, mês, trimestre, semestre, ano) |

> Todos os relatórios aceitam o parâmetro `?exportar=true` para download em Excel (.xlsx)

---

## 📊 Funcionalidades com Pandas

- **Agrupamento por categoria** — produtos organizados por categoria na listagem
- **Alerta de estoque baixo** — aviso automático quando a quantidade atinge o mínimo
- **Ranking de movimentações** — ordenação por produtos mais ou menos movimentados
- **Relatórios por período** — análise de entradas e saídas com filtro temporal
- **Exportação em Excel** — todos os relatórios podem ser exportados em `.xlsx`

---

## 🔒 Segurança

- Senhas criptografadas com **pwdlib**
- Autenticação via **JWT** com access e refresh token
- Validação de **CPF** com algoritmo oficial
- Validação de **telefone** via regex
- Cada usuário acessa apenas os próprios produtos

---

## 🗄️ Modelos do Banco

### Usuario
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| nome | String | Nome do usuário |
| sobrenome | String | Sobrenome |
| email | String | Email único |
| cpf | String | CPF único |
| telefone | String | Telefone único |
| status | Boolean | Ativo/Inativo |

### Produto
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| sku | String | Código único gerado automaticamente |
| nome | String | Nome padronizado (casefold) |
| categoria | Enum | Categoria do produto |
| preco_produto | Float | Preço de custo |
| preco_venda | Float | Preço de venda |
| quantidade | Integer | Quantidade em estoque |
| estoque_minimo | Integer | Limite mínimo para alerta |

### Movimentacao
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| produto_id | Integer | FK para Produto |
| tipo | Enum | entrada ou saida |
| quantidade | Integer | Quantidade movimentada |
| observacao | String | Contexto da movimentação |

---

## 👨‍💻 Autor

**Eric** — [github.com/ericjunq](https://github.com/ericjunq)
