from flask import Flask, render_template, request, redirect, url_for, flash
import json
from .instagram import Instagram
import os
import requests

app = Flask(__name__)
app.secret_key = "dev"

def load_accounts():
    DATA_DIR = os.path.dirname(__file__) + '/static/data'
    os.makedirs(DATA_DIR, exist_ok=True)
    account = []
    for folder in os.listdir(DATA_DIR):
        folder_path = os.path.join(DATA_DIR, folder)
        json_path = os.path.join(folder_path, f"{folder}.json")
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    account.append(data)
                except json.JSONDecodeError:
                    print(f"Erreur de lecture du fichier JSON: {json_path}")
    return account

@app.route('/')
def index():
    accounts = load_accounts()
    
    return render_template('index.html', accounts=accounts)

@app.route('/settings')
def settings():
    accounts = load_accounts()
    return render_template('settings.html', accounts=accounts, selected=None, settings=True)

@app.route('/add_account', methods=['POST'])
def add_account_route():
    # Récupération des données
    username = request.form['username']
    if username in load_accounts():
        flash(f"Déjà suivi", "defaite")
        return redirect(url_for('settings'))
    try:
        Instagram(username).save_user()
    except Exception as e:
        print(e)
        flash(f"Impossible de récupéré les donnée de « {username} »", "defaite")
        return redirect(url_for('index'))
    
    
    flash(f"✅ Le compte « {username} » a été ajouté avec succès !", "success")
    
    data = next((acc for acc in load_accounts() if acc['username'] == username), None)
    
    image_url = data['profile_picture_hd'] if data['profile_picture_hd'] else data['profile_picture']
    dest_folder = os.path.join(os.path.dirname(__file__), 'static', 'images')
    image_path = os.path.join(dest_folder, f"{username}.jpg")

    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            os.makedirs(dest_folder, exist_ok=True)
            with open(image_path, 'wb') as f:
                f.write(response.content)
        else:
            print("error resonse")
            flash(f"Impossible de récupéré la photo, u autre essaie sera fait pus tard", "defaite")
    except Exception as e:
        print("error jsp", e)
        flash(f"Impossible de récupéré la photo, u autre essaie sera fait pus tard", "defaite")
    return redirect(url_for('index'))

@app.route("/account/<username>")
def view_account(username):
    accounts = load_accounts()
    account = next((acc for acc in accounts if acc['username'] == username), None)
    
    views_data = {
        "2025-04-15": 1200,
        "2025-04-16": 1350,
        "2025-04-17": 1420,
        "2025-04-18": 1580,
        "2025-04-19": 1700,
    }

    follows_data = {
        "2025-04-15": 40,
        "2025-04-16": 45,
        "2025-04-17": 50,
        "2025-04-18": 55,
        "2025-04-19": 70,
    }

    views_data = {"2025-04-18": 1500, "2025-04-19": 1600, "2025-04-20": 1700}
    follows_data = {"2025-04-18": 50, "2025-04-19": 60, "2025-04-20": 70}
    likes_data = {"2025-04-18": 230, "2025-04-19": 310, "2025-04-20": 290}
    comments_data = {"2025-04-18": 45, "2025-04-19": 58, "2025-04-20": 52}

    messages = [
        {"sender": "lucie_d", "content": "Hey! Trop cool ton dernier post 😍", "date": "2025-04-20"},
        {"sender": "marc_insta", "content": "Tu fais des collabs ?", "date": "2025-04-19"},
        {"sender": "unknown", "content": "Check mon profil 🔥", "date": "2025-04-18"},
        {"sender": "lucie_d", "content": "Hey! Trop cool ton dernier post 😍", "date": "2025-04-20"},
        {"sender": "marc_insta", "content": "Tu fais des collabs ?", "date": "2025-04-19"},
        {"sender": "unknown", "content": "Check mon profil 🔥", "date": "2025-04-18"},
        {"sender": "lucie_d", "content": "Hey! Trop cool ton dernier post 😍", "date": "2025-04-20"},
        {"sender": "marc_insta", "content": "Tu fais des collabs ?", "date": "2025-04-19"},
        {"sender": "unknown", "content": "Check mon profil 🔥", "date": "2025-04-18"},
    ]

    fonction = ["publier"]


    return render_template("account.html", account=account,
                           views_data=views_data,
                           likes_data=likes_data,
                           comments_data=comments_data,
                           messages=messages,
                           follows_data=follows_data,
                           fonction=fonction)

@app.route("/account/<username>/tool", methods=["POST"])
def account_tool(username):
    func = request.form.get("tool_function")
    param_int = request.form.get("param_int", type=int)
    param_str = request.form.get("param_str", "").strip()

    print(f"Function: {func}, Param int: {param_int}, Param str: {param_str}")
    

    return redirect(url_for("view_account", username=username))

def boost_followers(username, multiplier=None, _=None):
    # Juste un exemple
    return f"Multiplicateur appliqué : {multiplier}"

def reset_daily_stats(username, *_):
    return "Stats journalières réinitialisées"

def analyze_engagement(username, threshold=None, tag=None):
    return f"Analyse faite avec seuil {threshold} et tag '{tag}'"


if __name__ == '__main__':
    app.run(debug=True)