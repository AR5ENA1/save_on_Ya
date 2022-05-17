import requests
import logging

logging.basicConfig(
    level='INFO',
    format='%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger('urllib3.connection').setLevel('WARNING')

class Vk:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }

    def search_foto(self, album_id):
        logger.info('Поиск фотографий начался')
        sort_foto = {}
        id = input("Пожалуйста, введите ID аккаунта: ")
        search_foto_url = self.url + 'photos.get'
        search_foto_params = {
            'owner_id': id,
            'album_id': album_id,
            'extended': '1',
        }
        fotos = requests.get(search_foto_url, params={**self.params, **search_foto_params})
        if fotos.status_code != 200:
            raise SystemExit(f"Error {fotos.json()['error']['error_code']}: {fotos.json()['error']['error_msg']}")
        else:
            if 'error' in fotos.json():
                raise SystemExit(f"Error: {fotos.json()['error']['error_msg']}")
            else:
                for param_foto in fotos.json()['response']['items']:
                    sorted_sizes = max(param_foto['sizes'], key=lambda x: x['height'] * x['width'])
                    if param_foto['likes']['count'] in sort_foto.keys():
                        sort_foto[param_foto['date']] = sorted_sizes['url']
                    else:
                        sort_foto[param_foto['likes']['count']] = sorted_sizes['url']
                logger.info(f'Найдено {len(sort_foto)} фотографий')
                return sort_foto

    def foto_on_avatar(self):
        logger.info('Поиск фотографий аватарке в Вконтакте')
        sort_foto = self.search_foto('profile')
        return sort_foto

    def foto_on_wall(self):
        logger.info('Поиск фотографий на стене в Вконтакте')
        sort_foto = self.search_foto('wall')
        return sort_foto
