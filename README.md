# Book.Nook

**Book.Nook** é uma aplicação web desenvolvida em Python com o framework **Flask**, criada para auxiliar amantes da leitura a organizarem e acompanharem seu progresso literário de forma prática, intuitiva e visualmente agradável.

---

## Visão Geral

O objetivo do projeto é proporcionar uma plataforma web onde leitores possam:

* Gerenciar seus livros e estantes;
* Acompanhar o progresso de leitura por livro;
* Avaliar e catalogar leituras;
* Personalizar informações do próprio perfil.

A interface prioriza usabilidade e responsividade para dispositivos móveis e desktop.

---

## Funcionalidades (Casos de Uso)

1. **Login / Logout** — autenticação de usuários com senhas protegidas.
2. **Pesquisar por um livro** — busca simples por título/autor.
3. **Adicionar à estante** — salvar livros na estante do usuário.
4. **Marcar progresso de leitura** — atualizar páginas lidas / porcentagem.
5. **Avaliar o livro** — deixar notas e comentários.
6. **Editar perfil** — atualizar dados do usuário.

---

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework:** Flask
* **Banco de dados:** SQLite (SQLAlchemy como ORM)
* **Autenticação / Segurança:** Flask-Bcrypt
* **Formulários:** Flask-WTF
* **Migrações:** Flask-Migrate / Alembic
* **Depuração:** Flask-DebugToolbar
* **Testes:** Pytest
* **Configuração:** Python-dotenv
* **Controle de versão:** Git + GitHub
* **Gestão Ágil:** Trello

---

## Estrutura do Projeto (prevista)

```
book.nook/
├── .env
├── .git/
├── .gitignore
├── README.md
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── blueprints/
│   │   ├── main/
│   │   │   └── routes.py
│   │   └── users/
│   │       └── routes.py
│   ├── static/         
│   └── templates/      
├── requirements.txt
├── run.py              
├── tests/              
└── venv/               
```

---

## Pré-requisitos

* Python 3.10+ (recomendado)
* Git

Recomenda-se criar um ambiente virtual para instalar dependências:

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Como executar

1. Clone o repositório:

```bash
git clone <URL-do-repositório>
cd BookNook
```

2. Crie e ative o ambiente virtual (veja seção anterior) e instale dependências:

```bash
pip install -r requirements.txt
```

3. Configure variáveis de ambiente (ex.: arquivo `.env`). Exemplos:

```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=sqlite:///booknook.db
SECRET_KEY=uma_chave_segura
```

4. Execute migrações (primeira execução):

```bash
flask db init    # só na primeira vez
flask db migrate -m "create tables"
flask db upgrade
```

5. Inicie a aplicação:

```bash
flask run
```

6. Abra no navegador: `http://127.0.0.1:5000/`.

---

## Processo Ágil (Cerimônias)

* **Planejamento da Sprint:** no início de cada sprint (Scrum Master / Equipe).
* **Weekly:** 1–2 vezes por semana, reuniões rápidas de alinhamento (Todos).
* **Revisão da Sprint:** ao final de cada sprint (Equipe).
* **Retrospectiva:** após a entrega, para melhorias contínuas (Equipe).

---

## Entregáveis

* Código-fonte completo no GitHub.
* Documentação técnica (README, diagrama de arquitetura, documentação de testes).
* Apresentação final do projeto.
* Checklist de funcionalidades testadas.
* Evidências de integração e testes automatizados.

