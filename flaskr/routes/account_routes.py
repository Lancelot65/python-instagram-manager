from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from ..utils.account_utils import load_accounts, load_data
from ..instagram import Instagram
from datetime import datetime, timedelta

bp = Blueprint('account_routes', __name__)
 
temp = []

@bp.route("/account/<username>")
def view_account(username):
    account = load_accounts(username)
    
    # Pour l'affichage initial, on charge les données des 30 derniers jours
    initial_data = get_filtered_account_data(username, 30)

    return render_template(
        "account.html",
        account=account,
        initial_data=initial_data
    )

@bp.route("/api/account/<username>/statistics")
def get_account_statistics(username):
    """API endpoint pour récupérer les statistiques filtrées par timeframe"""
    timeframe = request.args.get('timeframe', '30')
    
    try:
        # Récupérer les données filtrées
        if timeframe == 'all':
            days = None
        else:
            days = int(timeframe)
        
        data = get_filtered_account_data(username, days)
        
        return jsonify({
            'follows': data['follows_data'],
            'likes': data['likes_data'], 
            'comments': data['comments_data']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_filtered_account_data(username, days=None):
    """
    Récupère et filtre les données d'un compte selon la période spécifiée
    
    Args:
        username (str): Nom d'utilisateur du compte
        days (int): Nombre de jours à récupérer (None pour toutes les données)
    
    Returns:
        dict: Données formatées pour les graphiques
    """
    all_data = load_data(username)
    
    # Calculer la date limite si nécessaire
    if days is not None:
        cutoff_date = datetime.now() - timedelta(days=days)
    else:
        cutoff_date = None
    
    # Filtrer et traiter les données
    filtered_data = []
    for data in all_data:
        try:
            data_time = datetime.strptime(data['time'], "%y.%m.%d %H:%M:%S")
            
            # Appliquer le filtre de date si nécessaire
            if cutoff_date is None or data_time >= cutoff_date:
                filtered_data.append({
                    'time': data_time,
                    'original_data': data
                })
        except ValueError as e:
            print(f"Erreur de parsing de date pour {data.get('time', 'N/A')}: {e}")
            continue
    
    # Trier par date
    filtered_data.sort(key=lambda x: x['time'])
    
    # Préparer les données pour les graphiques
    follows_data = prepare_follows_data(filtered_data)
    likes_data = prepare_likes_data(filtered_data)
    comments_data = prepare_comments_data(filtered_data)
    
    return {
        'follows_data': follows_data,
        'likes_data': likes_data,
        'comments_data': comments_data
    }

def prepare_follows_data(filtered_data):
    """Prépare les données de followers pour le graphique"""
    labels = []
    values = []
    
    for item in filtered_data:
        time_str = item['time'].strftime("%Y-%m-%d %H:%M")
        follower_count = item['original_data'].get('follower', 0)
        
        labels.append(time_str)
        values.append(follower_count)
    
    return {
        'labels': labels,
        'values': values
    }

def prepare_likes_data(filtered_data):
    """Prépare les données de likes pour le graphique"""
    labels = []
    values = []
    
    for item in filtered_data:
        time_str = item['time'].strftime("%Y-%m-%d %H:%M")
        
        # Calculer le total des likes pour tous les reels à cette date
        total_likes = 0
        reels = item['original_data'].get('reel', [])
        for reel in reels:
            total_likes += reel.get('like', 0)
        
        labels.append(time_str)
        values.append(total_likes)
    
    return {
        'labels': labels,
        'values': values
    }

def prepare_comments_data(filtered_data):
    """Prépare les données de commentaires pour le graphique"""
    labels = []
    values = []
    
    for item in filtered_data:
        time_str = item['time'].strftime("%Y-%m-%d %H:%M")
        
        # Calculer le total des commentaires pour tous les reels à cette date
        total_comments = 0
        reels = item['original_data'].get('reel', [])
        for reel in reels:
            total_comments += reel.get('comment', 0)
        
        labels.append(time_str)
        values.append(total_comments)
    
    return {
        'labels': labels,
        'values': values
    }

def aggregate_data_by_period(filtered_data, period='daily'):
    """
    Agrège les données par période (daily, weekly, monthly)
    Utile pour de grandes quantités de données
    """
    if period == 'daily':
        date_format = "%Y-%m-%d"
    elif period == 'weekly':
        date_format = "%Y-W%U"  # Année-Semaine
    elif period == 'monthly':
        date_format = "%Y-%m"
    else:
        date_format = "%Y-%m-%d"
    
    aggregated = {}
    
    for item in filtered_data:
        period_key = item['time'].strftime(date_format)
        
        if period_key not in aggregated:
            aggregated[period_key] = {
                'followers': [],
                'likes': [],
                'comments': [],
                'dates': []
            }
        
        # Ajouter les données à l'agrégation
        aggregated[period_key]['followers'].append(
            item['original_data'].get('follower', 0)
        )
        
        # Calculer likes et comments
        reels = item['original_data'].get('reel', [])
        total_likes = sum(reel.get('like', 0) for reel in reels)
        total_comments = sum(reel.get('comment', 0) for reel in reels)
        
        aggregated[period_key]['likes'].append(total_likes)
        aggregated[period_key]['comments'].append(total_comments)
        aggregated[period_key]['dates'].append(item['time'])
    
    # Calculer les moyennes/totaux pour chaque période
    result = []
    for period_key, data in sorted(aggregated.items()):
        result.append({
            'period': period_key,
            'avg_followers': sum(data['followers']) / len(data['followers']) if data['followers'] else 0,
            'total_likes': sum(data['likes']),
            'total_comments': sum(data['comments']),
            'latest_date': max(data['dates']) if data['dates'] else None
        })
    
    return result

# Route optionnelle pour obtenir des statistiques agrégées
@bp.route("/api/account/<username>/aggregated-statistics")
def get_aggregated_account_statistics(username):
    """API endpoint pour récupérer les statistiques agrégées"""
    timeframe = request.args.get('timeframe', '30')
    period = request.args.get('period', 'daily')  # daily, weekly, monthly
    
    try:
        if timeframe == 'all':
            days = None
        else:
            days = int(timeframe)
        
        # Récupérer les données brutes
        all_data = load_data(username)
        
        # Filtrer par date
        if days is not None:
            cutoff_date = datetime.now() - timedelta(days=days)
        else:
            cutoff_date = None
        
        filtered_data = []
        for data in all_data:
            try:
                data_time = datetime.strptime(data['time'], "%y.%m.%d %H:%M:%S")
                if cutoff_date is None or data_time >= cutoff_date:
                    filtered_data.append({
                        'time': data_time,
                        'original_data': data
                    })
            except ValueError:
                continue
        
        # Agréger les données
        aggregated = aggregate_data_by_period(filtered_data, period)
        
        # Formater pour les graphiques
        labels = [item['period'] for item in aggregated]
        follows_values = [int(item['avg_followers']) for item in aggregated]
        likes_values = [item['total_likes'] for item in aggregated]
        comments_values = [item['total_comments'] for item in aggregated]
        
        return jsonify({
            'follows': {'labels': labels, 'values': follows_values},
            'likes': {'labels': labels, 'values': likes_values},
            'comments': {'labels': labels, 'values': comments_values}
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
