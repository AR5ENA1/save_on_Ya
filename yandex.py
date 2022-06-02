from tqdm import tqdm
import requests
import json

class Yandex_disk:
    url = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token):
        self.headers = {
            'Authorization': token
        }

    def create_folder(self):
        print('Создание новой папки на yandex')
        folder = input('Введите название создаваемой папки:\n>>> ')
        params = {
            'path': folder
        }
        req = requests.put(self.url, params=params, headers=self.headers)
        if req.status_code == 201:
            print(f'Папка с именем {folder} успешно создана!')
        else:
            raise SystemExit(f"Error: {req.json()['message']}")
        return folder

    def save_on_yandex_disk(self, photos, folder=None):
        print('Началась запись фотографий на yandex_disk')
        params = {
            'path': folder
        }
        for name, photo in tqdm(photos.items()):
            params = {
                'path': f'{folder}/{name}.jpg',
                'url': photo
            }
            req = requests.post(f'{self.url}/upload', params=params, headers=self.headers)
            if req.status_code != 202:
                raise SystemExit(f"Error: {req.json()['message']}")
        print('Фотографии успешно сохранены!')

    def save_in_json(self, folder):
        print('Локальное сохранение параметров загруженных фотографий в файл download.json')
        params = {
            'path': folder,
            'limit': "200"
        }
        req = requests.get(self.url, params=params, headers=self.headers)
        if req.status_code == 200:
            fotos = []
            for photo in tqdm(req.json()['_embedded']['items']):
                fotos.append({"file_name":photo['name'], "size":photo['size']})
            with open('download.json', 'w') as file:
                json.dump(fotos, file)
            print('Сохранение проведено успешно!')
        else:
            raise SystemExit(f"Error: {req.json()['message']}")
