# Bot de Cotação de Moedas com Python e BotCity 🤖

Automação RPA para buscar cotações de moedas no Google, baseada em uma lista CSV. Os dados coletados são organizados e salvos em um arquivo Excel, com integração completa ao BotCity Maestro.

---

## 👨🏻‍💻 Funcionalidades

- ✅ Leitura automatizada de uma planilha CSV com a lista de moedas.
- ✅ Busca no Google pela cotação e data atual de cada moeda.
- ✅ Extração e estruturação dos dados.
- ✅ Escrita dos dados atualizados em uma nova planilha Excel.
- ✅ Integração com o **BotCity Maestro** para controle e rastreamento de tarefas RPA.
- ✅ Uso de **docstrings e tipagem estática** com `mypy` para melhorar a legibilidade e manutenção.
- ✅ Suporte a **testes automatizados** com `pytest`.
- ✅ Execução via **Docker** com `docker-compose`.
- ✅ Registro de logs detalhados por execução em arquivos separados.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- [BotCity Web SDK](https://github.com/botcity-dev/botcity-framework-web-python)
- [BotCity Maestro SDK](https://github.com/botcity-dev/botcity-maestro-sdk)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)
- Google Chrome (modo headless)
- Pandas
- Docker & Docker Compose
- Pytest

---

## 📁 Estrutura do Projeto

```bash
.
├── app/                         # Módulos principais da automação
│   └── __init__.py 
│   └── bot_anonimo.py 
│   └── busca_cotacao.py 
│   └── manipula_arquivos.py
│   └── processamento_moedas.py 
├── build/                       # Scripts de build para diferentes SOs
│   └── build.sh
│   └── build.bat
│   └── build.ps1
├── files/                       # Arquivos gerados pelo BotCity Studio
│   └── bot-cotacao.zip          # Arquivo zip do bot
│   └── bot-cotacao.botproj
├── logs/                        # Pasta gerada dinamicamente com logs de execução
├── resources/                   # Arquivos de entrada e saída 
│   └── moedas.csv               # Arquivo de entrada com a lista de moedas
│   └── moedas_atualizadas.xlsx  # Arquivo gerado com cotações atualizadas
├── tests/                       # Testes unitários com pytest
│   └── __init__.py 
│   └── test_cotacao.py
│   └── test_arquivos.py
│   └── test_processamento.py
├── utils/                       # Utilitários de apoio (ex: captura de erro)
│   └── __init__.py 
│   └── screenshot_error.py
├── bot.py                       # Arquivo principal do bot
├── docker-compose.yml           # Orquestração Docker
├── Dockerfile                   # Dockerfile para o bot
├── requirements.txt             # Dependências do projeto
├── .gitignore
├── Mikefile
├── README.md
```

## 📦 Instalação

### 🔧 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- [Docker](https://www.docker.com/) (opcional, para execução containerizada)

---

## 💻 Rodando localmente

### 1. Clone este repositório

```bash
git clone https://github.com/seu-usuario/bot-cotacao-moedas.git
cd bot-cotacao-moedas
```

### 2. Crie e ative um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute o bot

```bash
python bot.py
```

### 5. Rodar o projeto no Docker

```bash
docker compose up
```

## 🐳 Rodando com Docker

### 1. Executar bot usando docker compose

```bash
docker compose up
```

---

## 🧪 Testes

**Execute os testes unitários com:**

```bash
pytest tests/
