import os
import json
import requests

def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_profile_picture(username, url):
    """Télécharge et sauvegarde l'image de profil d'un utilisateur Instagram."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        image_folder = os.path.join(os.path.dirname(__file__), f"../static/images")
        os.makedirs(image_folder, exist_ok=True)
        image_path = os.path.join(image_folder, f"{username}.jpg")
        with open(image_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Image de profil sauvegardée pour {username} à {image_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image de profil pour {username}: {e}")