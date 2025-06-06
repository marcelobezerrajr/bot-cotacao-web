# Bot de Cotação de Moedas com Python e BotCity 🤖

Este projeto é um bot de automação criado com [BotCity](https://botcity.dev/) que realiza buscas no Google para obter a cotação atual de diferentes moedas, com base em uma planilha CSV de entrada. Os resultados são extraídos e salvos em uma nova planilha CSV, automatizando completamente o processo de pesquisa de valores de câmbio.

---

## 👨🏻‍💻 Funcionalidades

- ✅ Leitura automatizada de uma planilha CSV com a lista de moedas.
- ✅ Busca no Google da cotação e data atual de cada moeda.
- ✅ Extração dos dados de forma estruturada.
- ✅ Escrita dos dados atualizados em uma nova planilha CSV.
- ✅ Integração com o **BotCity Maestro** para controle de tarefas RPA.
- ✅ Uso de **docstrings e tipagem** para melhorar a legibilidade e manutenção.
- ✅ Inclusão de **testes automatizados com `pytest`**.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- [BotCity Web SDK](https://github.com/botcity-dev/botcity-framework-web-python)
- [BotCity Maestro SDK](https://github.com/botcity-dev/botcity-maestro-sdk)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)
- Google Chrome
- Plugin CSV da BotCity

---

## 📁 Estrutura do Projeto

```bash
.
├── resources/
│   └── moedas_atualizadas.csv  # Arquivo gerado com cotações atualizadas
│   └── moedas.csv              # Arquivo de entrada com a lista de moedas
├── bot.py                      # Arquivo principal do bot
├── bot-cotacao.zip             # Arquivo zip do bot
├── bot-cotacao.botproj
├── build.bat
├── build.ps1
├── build.sh
├── README.md
├── requirements.txt
```

## 📦 Instalação

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
