import csv
import datetime
import logging
import os
import time
import requests
import schedule
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# 4. Configuração de LOGGING (Registra no console e no arquivo monitor_moedas.log)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("monitor_moedas.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Leitura de configurações sensíveis
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LIMITE_DOLAR = float(os.getenv("LIMITE_DOLAR", 5.25))
LIMITE_EURO = float(os.getenv("LIMITE_EURO", 5.80))

# 3. Controle de ESTADO para COOLDOWN (evita alertas duplicados)
# True = alerta ativo (já enviado), False = dentro da normalidade
estado_alertas = {"dolar": False, "euro": False}


def enviar_mensagem_telegram(mensagem):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        logging.error(
            "TELEGRAM_TOKEN ou CHAT_ID não configurados no arquivo .env"
        )
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown",
    }

    try:
        # Timeout para evitar que a requisição fique travada indefinidamente
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        logging.info("Notificação enviada com sucesso para o Telegram.")
    except requests.RequestException as e:
        logging.error(f"Falha ao enviar mensagem via Telegram: {e}")


def buscar_cotacoes():
    global estado_alertas
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"

    try:
        # 2. Timeout e validação do HTTP Status Code
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        dados = response.json()

        # Validação de estrutura da resposta
        if "USDBRL" not in dados or "EURBRL" not in dados:
            raise KeyError("Chaves 'USDBRL' ou 'EURBRL' ausentes na resposta.")

        dolar_valor = float(dados["USDBRL"]["bid"])
        dolar_var = dados["USDBRL"]["pctChange"]

        euro_valor = float(dados["EURBRL"]["bid"])
        euro_var = dados["EURBRL"]["pctChange"]

        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        logging.info(
            f"💵 Dólar: R$ {dolar_valor:.2f} ({dolar_var}%) | 💶 Euro: R$ {euro_valor:.2f} ({euro_var}%)"
        )

        salvar_historico(agora, dolar_valor, euro_valor)

        # 3. Lógica de Cooldown: Notifica apenas na MUDANÇA de estado (quando cruza a linha de limite)
        alertas = []

        # Checagem Dólar
        if dolar_valor <= LIMITE_DOLAR:
            if not estado_alertas["dolar"]:
                alertas.append(
                    f"🚨 *ALERTA DÓLAR!*\nCotação cruzou o limite: *R$ {dolar_valor:.2f}* (Limite: R$ {LIMITE_DOLAR:.2f})"
                )
                estado_alertas["dolar"] = True
        else:
            # Reseta o estado quando a moeda volta a subir
            if estado_alertas["dolar"]:
                logging.info(
                    "Dólar voltou a subir acima do limite. Estado de alerta resetado."
                )
                estado_alertas["dolar"] = False

        # Checagem Euro
        if euro_valor <= LIMITE_EURO:
            if not estado_alertas["euro"]:
                alertas.append(
                    f"🚨 *ALERTA EURO!*\nCotação cruzou o limite: *R$ {euro_valor:.2f}* (Limite: R$ {LIMITE_EURO:.2f})"
                )
                estado_alertas["euro"] = True
        else:
            if estado_alertas["euro"]:
                logging.info(
                    "Euro voltou a subir acima do limite. Estado de alerta resetado."
                )
                estado_alertas["euro"] = False

        # Disparo dos alertas pendentes
        if alertas:
            enviar_mensagem_telegram("\n\n".join(alertas))

    except requests.RequestException as e:
        logging.error(f"Erro de rede/timeout na API de cotações: {e}")
    except (KeyError, ValueError) as e:
        logging.error(f"Erro de formato nos dados da API: {e}")
    except Exception as e:
        logging.error(f"Erro inesperado no ciclo de monitoramento: {e}")


def salvar_historico(data_hora, dolar, euro):
    arquivo = "historico_cotacoes.csv"

    try:
        with open(arquivo, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Data_Hora", "Dolar_BRL", "Euro_BRL"])
    except FileExistsError:
        pass

    try:
        with open(arquivo, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([data_hora, dolar, euro])
    except Exception as e:
        logging.error(f"Erro ao salvar dados no CSV: {e}")


if __name__ == "__main__":
    logging.info("🚀 Monitor de Moedas Iniciado em Segundo Plano.")

    # Executa a primeira checagem imediata
    buscar_cotacoes()

    # Agenda a execução a cada 30 minutos
    schedule.every(30).minutes.do(buscar_cotacoes)

    while True:
        schedule.run_pending()
        time.sleep(1)