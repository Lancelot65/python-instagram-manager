from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = "dev"

def load_accounts():
    with open('.cache/account.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    accounts = load_accounts()
    selected_username = request.args.get('username')
    settings = request.args.get('settings') is not None
    selected_account = next((acc for acc in accounts if acc['username'] == selected_username), None) if selected_username else None
    return render_template('index.html', accounts=accounts, selected=selected_account, settings=settings)

@app.route('/settings')
def settings():
    accounts = load_accounts()
    return render_template('settings.html', accounts=accounts, selected=None, settings=True)

@app.route('/add_account', methods=['POST'])
def add_account_route():
    # Récupération des données
    username = request.form['username']
    password = request.form.get('password')  # ⚠️ stocké en clair (améliorable)
    flash(f"✅ Le compte « {username} » a été ajouté avec succès !", "success")
    # # Upload de l'image
    # image = request.files['image']
    # if image.filename == "":
    #     return "Aucune image sélectionnée", 400

    # image_filename = secure_filename(image.filename)
    # image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

    # # Création de l'objet compte
    # new_account = {
    #     "username": username,
    #     "password": password,  # peut être hashé si tu veux
    # }

    # # Sauvegarde
    # add_account(new_account, image_filename)
    print('add acount')

    return redirect(url_for('index'))

@app.route("/account/<username>")
def view_account(username):
    accounts = load_accounts()
    account = next((acc for acc in accounts if acc["username"] == username), None)
    
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

    fonction = [    ]


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