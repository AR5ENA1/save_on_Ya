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

    def search(self, urls, add_params):
        search_url = self.url + urls
        all_params = {**self.params, **add_params}
        full_params = self.get_sig(all_params)
        result = requests.get(search_url, params=full_params)
        if result.status_code != 200:
            raise SystemExit(f"Error {result.json()['error_code']}: {result.json()['error_msg']}")
        else:
            if 'error_code' in result.json():
                raise SystemExit(f"Error {result.json()['error_code']}: {result.json()['error_msg']}")
        return result

    def search_avatar(self, id, add_params=""):
        print('Поиск фотографий начался')
        search_avatar_url = 'photos/getPhotos'
        search_avatar_params = {
            'fid': id,
            'fields': 'user_photo.PIC_MAX, user_photo.LIKE_SUMMARY, user_photo.ID',
            'count': '100',
            'aid': add_params
        }
        photos = self.search(search_avatar_url, search_avatar_params)
        sort_photos = {}
        for photo in photos.json()['photos']:
            if photo['like_summary']['count'] in sort_photos:
                sort_photos[photo['id']] = photo['pic_max']
            else:
                sort_photos[photo['like_summary']['count']] = photo['pic_max']
        print(f'Найдено {len(sort_photos)} фотографий')
        return sort_photos

    def search_albums(self, id):
        print('Поиск альбомов начался')
        search_albums_url = 'photos/getAlbums'
        search_albums_params = {
            'fid': id,
            'format': 'json'
        }
        albums = self.search(search_albums_url, search_albums_params)
        sort_albums = {}
        k = 1
        for album in albums.json()['albums']:
            sort_albums[str(k)] = {'title':album['title'], 'aid': album['aid']}
            k += 1
        print(f'Найдено {len(sort_albums)} альбомов')
        return sort_albums

    def search_photo_in_albums(self, id):
        sort_albums = self.search_albums(id)
        print(f'Введите номер альбома, фотографии которого необходимо сохранить: ')
        for album in sort_albums.keys():
            print(f"{album} - {sort_albums[album]['title']}")
        num_album = input('>>> ')
        search_foto_in_album_params = sort_albums[num_album]['aid']
        sort_foto = self.search_avatar(id, search_foto_in_album_params)
        return sort_foto

    def get_sig(self, all_params):
        session_secret_key = all_params.pop('session_secret_key')
        full_params = all_params.copy()
        params = sorted(all_params.items())
        string = ''
        for x, y in params:
            string += f'{x}={y}'
        sig = hashlib.md5(f"{string}{session_secret_key}".encode()).hexdigest()
        full_params.update(sig=sig)
        return full_params
