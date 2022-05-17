import requests
import hashlib

class Ok:
    url = 'https://api.ok.ru/api/'

    def __init__(self, key):
        self.params = {
            'application_id': key['application_id'],
            'application_key': key['application_key'],
            'application_secret_key': key['application_secret_key'],
            'session_key': key['session_key'],
            'session_secret_key': key['session_secret_key']
        }

    def search_avatar(self):
        self.search_avatar_url = self.url + 'photos/getAlbums'
        search_avatar_params = {
            'fid': input('Введите ID: '),
            'format': 'json'
        }
        all_params = {**self.params, **search_avatar_params}

        session_secret_key = all_params.pop('session_secret_key')
        params = sorted(all_params.items())
        string = ''
        for x, y in params:
            string += f'{x}={y}'
        sig = hashlib.md5(f"{string}{session_secret_key}".encode()).hexdigest()
        all_params['sig'] = sig
        avatars = requests.get(search_avatar_url, params=all_params)
        return avatars.json()

    # def get_sig(self):




# 548962898298