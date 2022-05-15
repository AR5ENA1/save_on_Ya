import requests
from pprint import pprint
from tqdm import tqdm
import logging

logging.basicConfig(
    level='INFO',
    format='%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger('urllib3.connection').setLevel('WARNING')
# pprint(logging.Logger.manager.loggerDict)


class Vkontakte:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }

    def search_avatar(self):
        logger.info('Поиск фотографий на аватарке в контакте')
        sort_avatars = {}
        id = input("Пожалуйста, введите ID аккаунта: ")
        search_avatar_url = self.url + 'photos.get'
        search_avatar_params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': '1',
        }
        avatars = requests.get(search_avatar_url, params={**self.params, **search_avatar_params})
        if avatars.status_code != 200:
            raise SystemExit(f"Error: {avatars['error']['error_msg']}")
        else:
            for param_avatar in avatars.json()['response']['items']:
                sorted_sizes = max(param_avatar['sizes'], key=lambda x: x['height'] * x['width'])
                if param_avatar['likes']['count'] in sort_avatars.keys():
                    sort_avatars[param_avatar['date']] = sorted_sizes['url']
                else:
                    sort_avatars[param_avatar['likes']['count']] = sorted_sizes['url']
            logger.info(f'Найдено {len(sort_avatars)} фотографий')
            return sort_avatars

class Yandex:
    url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.headers = {
            'Authorization': token,
        }

    def create_folder(self):
        logger.info('Создание новой папки ')
        folder = input('Введите название создаваемой папки: ')
        params = {
            'path': folder
        }
        req = requests.put(self.url, params=params, headers=self.headers)
        if req.status_code == 201:
            logger.info(f'Папка с именем {folder} успешно создана!')
        else:
            raise SystemExit(f"Error: {req.json()['message']}")
        return folder

    def save_on_yandex_disk(self, sort_avatars, folder=None):
        logger.info('Началась запись фотографий на yandex_disk')
        params = {
            'path': folder
        }
        for name, foto in tqdm(sort_avatars.items()):
            params = {
                'path': f'{folder}/{name}.jpg',
                'url': foto
            }
            req = requests.post(f'{self.url}/upload', params=params, headers=self.headers)
            if req.status_code != 202:
                raise SystemExit(f"Error: {req.json()['message']}")
        logger.info('Фотографии успешно сохранены!')

if __name__ == '__main__':
    with open('token_vk.txt') as file:
        token_vk = file.read()
    with open('token_ya.txt') as file:
        token_ya = file.read()
    user_vk = Vkontakte(token_vk)
    user_ya = Yandex(token_ya)
    sort_avatars = user_vk.search_avatar()
    folder = user_ya.create_folder()
    user_ya.save_on_yandex_disk(sort_avatars, folder)


# 185797118
# 329067411
# 85797118