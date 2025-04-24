from flask import Blueprint, render_template
from ..utils.account_utils import load_accounts

bp = Blueprint('index', __name__)

@bp.route("/")
def index():
    # Charger tous les comptes
    accounts = load_accounts()
    return render_template("index.html", accounts=accounts)