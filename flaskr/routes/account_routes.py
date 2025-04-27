from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..utils.account_utils import load_accounts, load_data
from ..instagram import Instagram
from datetime import datetime

bp = Blueprint('account_routes', __name__)
 
temp = []

@bp.route("/account/<username>")
def view_account(username):
    all_data = load_data(username)
    account = load_accounts(username)

    # Initialize statistics
    views_data, likes_data, comments_data, follows_data = {}, {}, {}, {}

    for data in all_data:
        time = datetime.strptime(data['time'], "%y.%m.%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")

        follows_data[time] = data.get('follower', 0)
        views_data[time] = sum(reel.get('view', 0) for reel in data.get('reel', []))
        likes_data[time] = sum(reel.get('like', 0) for reel in data.get('reel', []))
        comments_data[time] = sum(reel.get('comment', 0) for reel in data.get('reel', []))

    return render_template(
        "account.html",
        account=account,
        views_data=views_data,
        likes_data=likes_data,
        comments_data=comments_data,
        follows_data=follows_data
    )