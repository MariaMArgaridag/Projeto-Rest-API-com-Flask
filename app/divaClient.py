import requests
import json

BASE_URL = "http://localhost:5000/cyber_threats"
WEBHOOK_URL = "http://localhost:6000/webhook"


# ======================= WEBHOOK ============================

def trigger_webhook(url, data):
    payload = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'DIVA-Webhook/1.0'
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code != 200:
            retry_later(url, data)
    except:
        retry_later(url, data)

def retry_later(url, data):
    print("Webhook falhou. Tentar mais tarde.")


# ======================= CLIENTE REST =======================

def get_infos():
    response = requests.get(BASE_URL)
    print("GET:", response.status_code)
    print(response.json()[:2])

def get_info(id):
    response = requests.get(f"{BASE_URL}/{id}")
    print("GET one:", response.status_code)
    print(response.json())

def create_info():
    data = {
        "country": "USA",
        "year": 2023,
        "attack_type": 2,
        "target_industry": 2,
        "financial_loss": 60.0,
        "affected_users": 1000,
        "attack_source": 2,
        "security_vulnerability": 2,
        "defense_mechanism": 2,
        "resolution_time": 63
    }

    response = requests.post(BASE_URL, json=data)
    print("POST:", response.status_code)
    print(response.json())

    # Opcional: disparar webhook apos criacao
    trigger_webhook(WEBHOOK_URL, data)

def update_info(id):
    data = {
        "country": "Portugal"
    }
    response = requests.put(f"{BASE_URL}/{id}", json=data)
    print("PUT:", response.status_code)
    print(response.json())

def delete_info(id):
    response = requests.delete(f"{BASE_URL}/{id}")
    print("DELETE:", response.status_code)


# ======================= MAIN ===============================

def menu():
    """Menu interativo"""
    while True:
        print("\n=== Cliente DIVA - Gestao de Incidentes ===")
        print("1. Listar todos os incidentes")
        print("2. Obter um incidente por ID")
        print("3. Criar novo incidente")
        print("4. Atualizar incidente")
        print("5. Apagar incidente")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opcao: ").strip()
        
        if opcao == "0":
            print("A sair...")
            break
        elif opcao == "1":
            get_infos()
        elif opcao == "2":
            incident_id = input("Digite o ID do incidente: ").strip()
            try:
                incident_id_int = int(incident_id)
            except ValueError:
                print("ID invalido")
                continue
            response = requests.get(f"{BASE_URL}/{incident_id_int}")
            print("GET one:", response.status_code)
            try:
                print(response.json())
            except ValueError:
                if response.text:
                    print(response.text)
                else:
                    print("Resposta vazia.")
        elif opcao == "3":
            create_info()
        elif opcao == "4":
            incident_id = input("Digite o ID do incidente a atualizar: ").strip()
            try:
                update_info(int(incident_id))
            except ValueError:
                print("ID invalido")
        elif opcao == "5":
            incident_id = input("Digite o ID do incidente a apagar: ").strip()
            try:
                delete_info(int(incident_id))
            except ValueError:
                print("ID invalido")
        else:
            print("Opcao invalida!")

if __name__ == "__main__":
    menu()
