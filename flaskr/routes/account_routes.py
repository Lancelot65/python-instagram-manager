from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..utils.account_utils import load_accounts
from ..instagram import Instagram
from datetime import datetime

bp = Blueprint('account_routes', __name__)

@bp.route("/account/<username>")
def view_account(username):
    all_data_account = load_accounts(username, True)[0]
    account = load_accounts(username)

    # Initialize statistics
    views_data, likes_data, comments_data, follows_data = {}, {}, {}, {}

    for data in all_data_account:
        temp_data = all_data_account[data]
        time = datetime.strptime(data, "%y.%m.%d").strftime("%Y-%m-%d")

        follows_data[time] = temp_data.get('followed', 0)
        views_data[time] = sum(reel.get('view', 0) for reel in temp_data.get('reel', []))
        likes_data[time] = sum(reel.get('like', 0) for reel in temp_data.get('reel', []))
        comments_data[time] = sum(reel.get('comment', 0) for reel in temp_data.get('reel', []))

    return render_template(
        "account.html",
        account=account,
        views_data=views_data,
        likes_data=likes_data,
        comments_data=comments_data,
        follows_data=follows_data,
        fonction=['test']
    )

@bp.route("/account/<username>/tool", methods=["POST"])
def account_tool(username):
    func = request.form.get("tool_function")
    param_int = request.form.get("param_int", type=int)
    param_str = request.form.get("param_str", "").strip()

    print(f"Function: {func}, Param int: {param_int}, Param str: {param_str}")
    return redirect(url_for("account_routes.view_account", username=username))