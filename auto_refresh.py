from flaskr.utils.account_utils import load_accounts
from flaskr.instagram import Instagram
from datetime import datetime, timedelta


def updates():
    data = load_accounts()
    for account in data:
        username = account['username']
        
        last_download_time = datetime.strptime(account['last_download'], "%y.%m.%d %H:%M:%S")
        
        if datetime.now() - last_download_time >= timedelta(hours=1, minutes=55):
            try:
                insta = Instagram(username)
                insta.update_user()
            except Exception as e:
                print(e)
        else:
            print("don't need to update")
updates()
