import os
import json
from datetime import datetime

def load_accounts(username=None, all=False):
    DATA_DIR = os.path.join(os.path.dirname(__file__), '../static/data')
    os.makedirs(DATA_DIR, exist_ok=True)
    accounts = []

    for folder in os.listdir(DATA_DIR):
        folder_path = os.path.join(DATA_DIR, folder)
        json_path = os.path.join(folder_path, f"{folder}.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if username and folder == username:
                        return [data] if all else get_last_data(data)
                    
                    if all:
                        accounts.append(data)
                    else:
                        accounts.append(get_last_data(data))
                except json.JSONDecodeError:
                    print(f"Erreur de lecture du fichier JSON: {json_path}")
    return accounts

def get_last_data(data):
    dates = data.keys()
    return data[max(dates)]