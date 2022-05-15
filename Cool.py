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


class Vk:
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
        avatars = requests.get(search_avatar_url, params={**self.params, **search_avatar_params}).json()
        for param_avatar in avatars['response']['items']:
            sorted_sizes = max(param_avatar['sizes'], key=lambda x: x['height'] * x['width'])
            if param_avatar['likes']['count'] in sort_avatars.keys():
                sort_avatars[param_avatar['date']] = sorted_sizes['url']
            else:
                sort_avatars[param_avatar['likes']['count']] = sorted_sizes['url']
        logger.info(f'Найдено {len(sort_avatars)} фотографий')
        return sort_avatars

    def search_and_save_on_yandex_disk(self):
        sort_avatars = self.search_avatar()
        logger.info('Началась запись фотографий на yandex_disk')
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        with open('token_ya.txt') as file_object:
            token_ya = file_object.read()
        headers = {'Authorization': token_ya}
        requests.put(url, params={'path': 'foto'}, headers=headers)
        for name, foto in tqdm(sort_avatars.items()):
            params = {
                'path': f'/foto/{name}.jpg',
                'url': foto
            }
            requests.post(f'{url}/upload', params=params, headers=headers)
        logger.info('Фотографии успешно сохранены!')

if __name__ == '__main__':
    with open('token_vk.txt') as file:
        token_vk = file.read()
    user_vk = Vk(token_vk)
    user_vk.search_and_save_on_yandex_disk()

# '185797118'
