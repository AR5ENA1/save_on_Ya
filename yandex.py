from tqdm import tqdm
import logging
import requests

logging.basicConfig(
    level='INFO',
    format='%(asctime)s %(module)s %(levelname)s %(lineno)d %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger('urllib3.connection').setLevel('WARNING')

class Yandex_disk:
    url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.headers = {
            'Authorization': token,
        }

    def create_folder(self):
        logger.info('Создание новой папки на yandex')
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