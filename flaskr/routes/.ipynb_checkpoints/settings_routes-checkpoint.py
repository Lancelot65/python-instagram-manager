from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..utils.account_utils import load_accounts
from ..utils.data_utils import save_profile_picture
from ..instagram import Instagram

bp = Blueprint('settings_routes', __name__)

@bp.route('/settings')
def settings():
    accounts = load_accounts()
    return render_template('settings.html', accounts=accounts, selected=None, settings=True)

@bp.route('/add_account', methods=['POST'])
def add_account_route():
    username = request.form['username']
    all_user = [data['username'] for data in load_accounts()]
    if username in all_user:
        flash(f"Already follow", "success")
        return redirect(url_for('index_routes.index'))
    try:
        Instagram(username).save_user()
        data = load_accounts(username=username)
        profile_picture_url = data["profile_picture_hd"] or data["profile_picture"]
        if profile_picture_url:
            save_profile_picture(username, profile_picture_url)
        flash(f"✅ Le compte « {username} » a été ajouté avec succès !", "success")
    except Exception as e:
        print(e)
        flash(f"Impossible de récupéré les donnée de « {username} »", "defaite")
    return redirect(url_for('index_routes.index'))