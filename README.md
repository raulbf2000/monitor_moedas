# 📈 Monitor de Cotações de Moedas em Tempo Real

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=for-the-badge&logo=telegram)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-brightgreen?style=for-the-badge)

Uma automação robusta desenvolvida em Python para monitoramento contínuo das cotações do **Dólar (USD)** e **Euro (EUR)** em relação ao **Real (BRL)**, com sistema de alertas em tempo real via **Telegram** e salvamento de histórico em planilha **CSV**.

---

## 🚀 Funcionalidades

- **📈 Consumo de API em Tempo Real:** Obtém cotações atualizadas diretamente da [AwesomeAPI](https://docs.awesomeapi.com.br/).
- **🚨 Alertas Inteligentes via Telegram:** Notifica instantaneamente no celular quando a moeda cai abaixo do limite configurado.
- **🛡️ Mecanismo de Cooldown (Anti-Spam):** Dispara alerta apenas quando a cotação **cruza** o limite estabelecido, evitando notificações duplicadas a cada ciclo.
- **📊 Histórico Persistente em CSV:** Registra automaticamente a data, hora e cotações no arquivo `historico_cotacoes.csv`.
- **🔐 Segurança com Variáveis de Ambiente:** Utiliza `python-dotenv` para manter chaves e tokens totalmente protegidos fora do código-fonte.
- **📝 Sistema de Logging:** Logs estruturados em console e no arquivo `monitor_moedas.log` para monitoramento de saúde do script e auditoria de erros.
- **⏱️ Agendamento Automático:** Execução em background configurável (ex: a cada 30 minutos) através da biblioteca `schedule`.

---

## 🛠️ Tecnologias Utilizadas

- **[Python](https://www.python.org/)** — Linguagem principal
- **[Requests](https://requests.readthedocs.io/)** — Requisições HTTP com suporte a timeouts e tratamento de erros
- **[Schedule](https://schedule.readthedocs.io/)** — Agendador de tarefas leve
- **[Python-Dotenv](https://pypi.org/project/python-dotenv/)** — Gerenciamento de variáveis de ambiente
- **[Telegram Bot API](https://core.telegram.org/bots/api)** — Notificações push em tempo real

---

## 📁 Estrutura do Projeto

```text
monitor_moedas/
├── .env.example              # Modelo de variáveis de ambiente (sem dados sensíveis)
├── .gitignore                # Arquivos ignorados pelo Git (protege o .env real)
├── monitor_moedas.py         # Script principal da aplicação
└── README.md                 # Documentação do projeto

Como Executar o Projeto
Prerequisitos
Python 3.10 ou superior instalado.

Um Bot no Telegram criado via @BotFather e o seu CHAT_ID.

1. Clonar o Repositório
git clone [https://github.com/raulbf2000/monitor_moedas.git](https://github.com/raulbf2000/monitor_moedas.git)
cd monitor_moedas

2. Instalar as Dependências
pip install requests schedule python-dotenv

3. Configurar as Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto com base no modelo .env.example:

TELEGRAM_TOKEN=seu_token_do_bot_aqui
CHAT_ID=seu_chat_id_aqui
LIMITE_DOLAR=5.25
LIMITE_EURO=5.80

4. Executar o Monitor

python monitor_moedas.py

Licença
Este projeto está sob a licença MIT. Sinta-se livre para usar, estudar e aprimorar!

Desenvolvido por Raul 🚀