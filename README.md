# Documentação Técnica — Cyber Threats API

## Tecnologias Utilizadas

- **Python 3.13**
- **Flask** — Framework web
- **pip** — Gerenciador de dependências
- **MySQL** — Banco de dados
- **Virtual Environment (venv)** — Isolamento de dependências
- **Variáveis de ambiente (.env)** — Configuração segura
- **OpenAPI 3** — Documentação da API (openapi.yaml)

---

## Estrutura do Projeto

```
app/
├── controller/     # Rotas HTTP e endpoints
├── service/        # Regras de negócio e lógica da aplicação
├── repository/     # Acesso e manipulação do banco de dados
├── database.py     # Configuração e conexão com o MySQL
└── main.py         # Inicialização da aplicação Flask
openapi.yaml        # Documentação OpenAPI da API
.env                # Variáveis de ambiente
venv/               # Ambiente virtual Python
```

---

## Configuração do Ambiente

### 1. Criar e ativar o ambiente virtual

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python3 -m venv venv
venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Configuração do Banco de Dados

Crie o arquivo `.env` na raiz do projeto com as seguintes variáveis, adaptando para seu banco de dados:

```env
DB_HOST=localhost
DB_USERNAME=root
DB_PASSWORD=''
DB_DATABASE=flask
```

---

## Executar o Projeto

Com o ambiente virtual ativado, execute:

```bash
python app/main.py

ou

python -m app.main
```

A API ficará disponível em:

```
http://localhost:5000
```

Testes de carga:
 instalar o programa, por vezes pode já vir no Windows

https://www.postman.com/downloads/

verificar se está tudo bem:

	http://localhost:5000/

Rotas básicas:

	http://localhost:5000/attack_types/

	http://localhost:5000/defense_mechanisms/

	http://localhost:5000/security_vulnerabilities/
	
	http://localhost:5000/target_industries/

	http://localhost:5000/cyber_threats/

Para estatísticas:

	http://localhost:5000/cyber_threats/attack_types

	http://localhost:5000/cyber_threats/defense_mechanism

	http://localhost:5000/cyber_threats/security_vulnerability

	http://localhost:5000/cyber_threats/target_industry

Documentação:

	http://localhost:5000/apidocs/



Através dos testes de carga, verificamos que é uma carga sequencial
	-velocidade da API 
	-O tempo aumenta quando se faz várias iterações (ex: vai depender do número de pedidos

Neste caso se os pedidos falharam poderemos ter erros como: 400, 404 e 500.
Que poderá resultar em validações mal feitas e erros no backend, quando existem muitas chamadas.

Poderá haver problemas na validação dos campos, dados que quebram o serviço, mensagens de erro inconsistentes.

O GET é mais rápido que o POST (Lento, pode existir problema na escrita na Base de Dados)

As rotas básicas são mais rápidas do que os endpoints das estatísticas .
