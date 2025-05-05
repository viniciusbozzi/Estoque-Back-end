# 📦 API de Produtos e Movimentações

API REST desenvolvida com **FastAPI** para gerenciar **cadastro de produtos**, **movimentações de entrada e saída**, e **controle de estoque**. Utiliza **MySQL**, **SQLAlchemy** e separação em camadas (models, schemas, routers, settings).

---

## 🚀 Tecnologias

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/)
- [Pydantic](https://docs.pydantic.dev/)

---

## 📁 Estrutura de Diretórios

```bash
app/
├── models/
│ ├── product.py
│ └── movement.py
├── schemas/
│ ├── product.py
│ └── movement.py
├── routers/
│ ├── product.py
│ └── movement.py
│ └── stock.py
├── settings/
│ └── .env
│ └── config.py
│ └── database.py
├── main.py
```


## 📚 Endpoints

Produto /product

| Método | Rota             | Descrição               |
| ------ | ---------------- | ----------------------- |
| GET    | `/read`          | Lista todos os produtos |
| POST   | `/create`        | Cadastra novo produto   |
| GET    | `/read/{name}`   | Busca produto pelo nome |
| PUT    | `/update/{name}` | Atualiza produto        |
| DELETE | `/delete/{name}` | Remove produto          |


Movimentações /movement
| Método | Rota                    | Descrição                                |
| ------ | ----------------------- | ---------------------------------------- |
| POST   | `/create`               | Cria entrada ou saída de produto         |
| GET    | `/all`                  | Lista todas as movimentações             |


Stock /stock
| Método | Rota                    | Descrição                                |
| ------ | ----------------------- | ---------------------------------------- |
| GET    | `/details/{product_id}` | Retorna dados + movimentações do produto |


---

## ⚙️ Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/viniciusbozzi/Estoque-Back-end
cd Estoque-Back-end
```

### 2. Crie o ambiente virtual e Instale as dependências
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "fastapi[standard]"
pip install pydantic_settings
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
pip install SQLAlchemy
pip install mysqlclient
```

### 3. Configure o banco de dados
Atualize o arquivo .env com os dados da sua conexão MySQL:

```bash
# ~/Estoque-Back-end/app/settings/.env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
MYSQL_DATABASE=seu_banco
```

OBS: Para subir o banco de dados via docker: https://github.com/EstudosCpid/mini-curso-backend-2025/blob/main/Roteiro_Mini-Curso-Backend.md#7-banco-de-dados (Siga o passo 7)


### 4. Execute as migrações com Alembic
```bash
# ~/Estoque-Back-end$
pip install alembic
alembic init alembic
```

#### 4.1 Configuração

Altere o arquivo `env.py` para incluir as configurações necessárias.

```bash
# ~/Estoque-Back-end/alembic/env.py

#  ... código omitido

# from alembic import context

from app.settings.database import SQLALCHEMY_DATABASE_URL

# ... código omitido 

#config = context.config

config.set_main_option(
    "sqlalchemy.url",
    SQLALCHEMY_DATABASE_URL,
)

#target_metadata = None

from app.models import product, movement 
target_metadata = product.Base.metadata
target_metadata = movement.Base.metadata

# ... código omitido 
```

#### 4.2 Realizar migration

Execute o comando abaixo a partir da raiz do projeto:

```bash
alembic revision --autogenerate -m "initial" --rev-id 1
```

Para criar as tabelas no banco de acordo com a revision gerada, execute o comando abaixo:
```bash
alembic upgrade head
```

### 5 Executando a aplicação
```bash
fastapi dev app/main.py
```

Acesse o URL http://localhost:8000/docs para testar a API.

