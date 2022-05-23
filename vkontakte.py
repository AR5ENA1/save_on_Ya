import requests

class Vk:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }

    def search_photo(self, id, add_param, vk_metod='photos.get'):
        sort_photo = {}
        print('Поиск фотографий начался')
        search_photo_url = self.url + vk_metod
        search_photo_params = {
            'owner_id': id,
            'extended': '1',
        }
        photos = requests.get(search_photo_url, params={**self.params, **search_photo_params, **add_param})
        if photos.status_code != 200:
            raise SystemExit(f"Error {photos.json()['error']['error_code']}: {photos.json()['error']['error_msg']}")
        else:
            if 'error' in photos.json():
                raise SystemExit(f"Error: {photos.json()['error']['error_msg']}")
            else:
                for param_photo in photos.json()['response']['items']:
                    sorted_sizes = max(param_photo['sizes'], key=lambda x: x['height'] * x['width'])
                    if param_photo['likes']['count'] in sort_photo.keys():
                        sort_photo[param_photo['date']] = sorted_sizes['url']
                    else:
                        sort_photo[param_photo['likes']['count']] = sorted_sizes['url']
                print(f'Найдено {len(sort_photo)} фотографий')
                return sort_photo

    def photo_on_avatar(self, id):
        print('Поиск фотографий на аватарке')
        add_param = {'album_id': 'profile'}
        sort_photo = self.search_photo(id, add_param)
        return sort_photo

    def photo_on_wall(self, id):
        print('Поиск фотографий на стене')
        add_param = {'album_id': 'wall'}
        sort_photo = self.search_photo(id, add_param)
        return sort_photo

    def photo_in_album(self, id):
        print('Поиск фотографий в альбомах')
        add_param = {
            'photo_sizes': '1',
            'no_service_albums': '1',
            'count': '200'
        }
        sort_photo = self.search_photo(id, add_param, 'photos.getAll')
        return sort_photo

