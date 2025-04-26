from flask import Blueprint, redirect, url_for, flash
from ..utils.account_utils import load_accounts
from ..instagram import Instagram
from datetime import datetime

bp = Blueprint('refresh_routes', __name__)

@bp.route('/refresh')
def daily_check():
    data = load_accounts()
    for account in data:
        username = account['username']
        if datetime.now().strftime("%y.%m.%d") != account['last_download']:
            try:
                Instagram(username).save_user()
                flash(f"{username} update", "success")
            except Exception as e:
                print(e)
                flash(f"Impossible de récupéré journaliére les donnée de « {account['username']} »", "bad")
    return redirect(url_for('index_routes.index'))
