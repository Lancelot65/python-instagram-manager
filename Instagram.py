from instagrapi import Client
import json
from pathlib import Path
import logging
import random
import time

class insatgram_public:
	def __init__(self, instagram_name):
		self.cl = Client()
		self.cl.delay_range = [1, 3]
		self.open_data_file()
		self.user_info = self.cl.user_info_by_username(instagram_name)

    def get_photo(self):
		url = self.user&


class instagram_private:
    def __init__(self, account):
        self.account = account
        self.cl = Client()
        self.cl.delay_range = [1, 3]
        self.try_log()

      def try_log(self):
        try:
            cache_dir = Path('.cache')
            if not cache_dir.exists():
                cache_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"No .cache directory, make one")
                return
			

            session_file = cache_dir / f"{self.account}_session.json"
            if session_file.is_file():
                self.cl.load_settings(str(session_file))
                logger.info('LOG : use session')
            self.open_data_file()

            self.cl.login(self.instagram_name, self.instagram_password)
            logger.info('LOG : connected')
            # self.cl.get_timeline_feed()

            if not session_file.is_file():
                self.cl.dump_settings(str(session_file))
                logger.info('LOG : session save')
            self.cl.get_timeline_feed()
            
        except Exception as e:
            logger.error(f"LOG : Something went wrong, please connect manually: {str(e)}")

    
    def open_data_file(self):
        account_file = Path(".cache") / "account.json"  # Utilisation de Path pour le fichier account.json
        with account_file.open('r', encoding='utf-8') as file:
            data = json.load(file)
        self.instagram_name = data[self.account]["instagram_name"]
        self.instagram_password = data[self.account]["password"]

        logger.info('LOG : load username/password')
    
