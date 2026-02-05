# Book.Nook 📚

**Book.Nook** é uma aplicação web "Full Stack" para gestão de bibliotecas pessoais. O sistema consome a API do Google Books para permitir que utilizadores pesquisem obras, organizem estantes virtuais e acompanhem o progresso de leitura em tempo real.

![Status do Projeto](https://img.shields.io/badge/Status-Concluído-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)

## 📸 Demonstração
<img width="1680" height="995" alt="image" src="https://github.com/user-attachments/assets/28b9fc0e-e079-4c1a-b369-e8a31dfd7593" />

## 🚀 Funcionalidades Técnicas

* **Integração de API Externa:** Consumo da Google Books API para busca e recuperação de metadados de livros (títulos, autores, capas, contagem de páginas).
* **Autenticação Robusta:** Sistema completo de Login/Registo utilizando `Flask-Login` e hash de senhas com `Bcrypt`.
* **Gestão de Estado:** Acompanhamento de progresso de leitura (página atual vs. total) com feedback visual (barras de progresso).
* **CRUD Completo:** Criação, leitura, atualização e remoção de livros na estante pessoal do utilizador.
* **Validações de Segurança:** Validação de inputs no Back-end (Regex para senhas fortes e emails) e proteção contra CSRF via `Flask-WTF`.

## 🛠️ Stack Tecnológico

O projeto foi construído utilizando a arquitetura **MVC (Model-View-Controller)**:

* **Backend:** Python 3, Flask (Blueprints & Application Factory Pattern).
* **Base de Dados:** SQLite com SQLAlchemy (ORM).
* **Frontend:** Bootstrap 5, Jinja2 Templates, CSS3 Personalizado (Glassmorphism UI).
* **Serviços:** `requests` para chamadas HTTP externas.

## ⚙️ Como Executar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/frsrodrigobocayuva/book.nook.git](https://github.com/frsrodrigobocayuva/book.nook.git)
    cd book.nook
    ```

2.  **Configure o Ambiente Virtual:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um ficheiro `.env` na raiz do projeto e adicione a sua chave (necessária para a busca de livros):
    ```env
    GOOGLE_BOOKS_API_KEY="Sua_Chave_da_Google_API_Aqui"
    SECRET_KEY="sua_chave_secreta_aqui"
    ```

5.  **Execute a aplicação:**
    ```bash
    flask run
    ```
    Aceda em `http://127.0.0.1:5000`

---
Desenvolvido por: [Rodrigo Bocayuva](https://www.linkedin.com/in/rodrigobocayuva), [Lucas Fischer](https://www.linkedin.com/in/lucasfischerw/), [Mel Alves](https://www.linkedin.com/in/melalves/), [Markus Lopes](https://www.linkedin.com/in/markus-lopes-2b3102268/) e David Xavier.
