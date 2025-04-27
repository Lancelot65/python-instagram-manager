import os
import json
from datetime import datetime

def load_accounts(username=None):
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../static/profiles')
    os.makedirs(DATA_DIR, exist_ok=True)
    accounts = []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(DATA_DIR, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        file_username = os.path.splitext(filename)[0]  # Enlève ".json" du nom de fichier

                        if username and file_username == username:
                            return data
                        
                        accounts.append(data)
                    except json.JSONDecodeError:
                        print(f"Erreur de lecture du fichier JSON: {file_path}")
    return accounts

def load_data(username):
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../static/data')
    os.makedirs(DATA_DIR, exist_ok=True)
    data = []
    
    file_path = os.path.join(DATA_DIR, f"{username}.json")
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    
    return data