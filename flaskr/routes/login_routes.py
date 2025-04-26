from flask import Blueprint, request, session, redirect, url_for


bp = Blueprint('login_routes', __name__)

PASSWORD = "root"

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index_routes.index'))
        else:
            return '''
                <h2>Mot de passe incorrect</h2>
                <form method="post">
                    <input type="password" name="password" placeholder="Mot de passe">
                    <input type="submit" value="Se connecter">
                </form>
            '''
    return '''
        <h2>Connexion</h2>
        <form method="post">
            <input type="password" name="password" placeholder="Mot de passe">
            <input type="submit" value="Se connecter">
        </form>
    '''

@bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('auth_routes.login'))
