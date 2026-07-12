import undetected_chromedriver as uc
import time
import random
import pyautogui
import csv
import re
import os

INPUT_CSV = "data.csv"
OUTPUT_CSV = "resultados_consulta_obito.csv"

POS_CPF = (670, 470)
POS_DATA = (670, 520)
POS_CAPTCHA = (930, 460)
POS_CONSULTAR = (1100, 670)

DELAY_MIN = 0.08
DELAY_MAX = 0.19
ESPERA_APOS_CONSULTA = 8

def digitar(texto):
    for char in texto:
        pyautogui.typewrite(char)
        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))
    time.sleep(0.8)

def extrair_informacoes(page_source):
    resultado = {
        "nome": "",
        "cpf": "",
        "nascimento": "",
        "data_obito": "",
        "status": "Sem registro de óbito"
    }

    nome_match = re.search(r'Nome:\s*<b>(.*?)</b>', page_source, re.IGNORECASE | re.DOTALL)
    if nome_match:
        resultado["nome"] = nome_match.group(1).strip()

    nasc_match = re.search(r'Data de Nascimento:\s*<b>(\d{2}/\d{2}/\d{4})', page_source, re.IGNORECASE)
    if nasc_match:
        resultado["nascimento"] = nasc_match.group(1).strip()

    if re.search(r'TITULAR FALECIDO', page_source, re.IGNORECASE):
        resultado["status"] = "ÓBITO ENCONTRADO"

        ano_match = re.search(r'Ano de óbito:\s*<b>(\d{4})', page_source, re.IGNORECASE)
        if ano_match:
            resultado["data_obito"] = ano_match.group(1)
        else:
            data_match = re.search(r'(\d{2}/\d{2}/\d{4})', page_source)
            if data_match and "nascimento" not in data_match.group(0).lower():
                resultado["data_obito"] = data_match.group(1)
    
    return resultado

print("🚀 Iniciando consulta com extração atualizada...\n")

if not os.path.exists(INPUT_CSV):
    print(f"ERRO: {INPUT_CSV} não encontrado!")
    exit(1)

with open(INPUT_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    registros = list(reader)

print(f"{len(registros)} registros para processar.\n")

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options)

with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["nome", "cpf", "nascimento", "data_obito", "status"])
    writer.writeheader()

try:
    for i, row in enumerate(registros, 1):
        cpf_raw = row.get('CPF') or row.get('cpf') or ""
        data_raw = row.get('DATA_NASC') or row.get('data_nasc') or ""
        
        cpf = re.sub(r'\D', '', str(cpf_raw))
        data_nasc = re.sub(r'\D', '', str(data_raw))
        
        print(f"[{i}/{len(registros)}] CPF: {cpf}")
        
        try:
            driver.get("https://servicos.receita.fazenda.gov.br/servicos/cpf/consultasituacao/consultapublica.asp")
            time.sleep(5)

            pyautogui.moveTo(POS_CPF[0], POS_CPF[1], duration=0.6)
            pyautogui.click()
            time.sleep(0.8)
            digitar(cpf)

            pyautogui.moveTo(POS_DATA[0], POS_DATA[1], duration=0.6)
            pyautogui.click()
            time.sleep(0.8)
            digitar(data_nasc)
    
            pyautogui.moveTo(POS_CAPTCHA[0], POS_CAPTCHA[1], duration=0.8)
            pyautogui.click()
            time.sleep(8)

            pyautogui.moveTo(POS_CONSULTAR[0], POS_CONSULTAR[1], duration=0.6)
            pyautogui.click()
            time.sleep(ESPERA_APOS_CONSULTA)
            
            info = extrair_informacoes(driver.page_source)
            info["cpf"] = cpf
            
            with open(OUTPUT_CSV, 'a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["nome", "cpf", "nascimento", "data_obito", "status"])
                writer.writerow(info)
            
            print(f"   → {info['status']} | Nome: {info['nome'][:40]} | Óbito: {info.get('data_obito', 'N/A')}")
            
        except Exception as e:
            print(f"   → ERRO: {e}")
            with open(OUTPUT_CSV, 'a', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["nome", "cpf", "nascimento", "data_obito", "status"])
                writer.writerow({
                    "nome": "ERRO",
                    "cpf": cpf,
                    "nascimento": data_nasc,
                    "data_obito": "",
                    "status": f"ERRO: {str(e)[:80]}"
                })
        
        if i < len(registros):
            time.sleep(random.uniform(15, 25))
            
except Exception as e:
    print(f"\nErro geral: {e}")
finally:
    driver.quit()