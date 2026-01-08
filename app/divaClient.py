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

    # Opcional: disparar webhook após criação
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

if __name__ == "__main__":
    get_infos()
    get_info(2)
    create_info()
    update_info(2)
    delete_info(140)
