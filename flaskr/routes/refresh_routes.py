from flask import Blueprint, redirect, url_for, flash
from ..utils.account_utils import load_accounts
from ..instagram import Instagram
from datetime import datetime, timedelta

bp = Blueprint('refresh_routes', __name__)

@bp.route('/refresh')
def daily_check():
    data = load_accounts()
    for account in data:
        username = account['username']
        
        last_download_time = datetime.strptime(account['last_download'], "%y.%m.%d %H:%M:%S")
        
        if datetime.now() - last_download_time >= timedelta(hours=2):
            try:
                insta = Instagram(username)
                insta.update_user()
                flash(f"Les données de « {username} » ont été mises à jour.", "success")
            except Exception as e:
                print(e)
                flash(f"Impossible de mettre à jour les données de « {username} ».", "danger")
    
    return redirect(url_for('index_routes.index'))