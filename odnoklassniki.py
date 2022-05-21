import requests
import hashlib
from  pprint import pprint

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
        search_avatar_url = self.url + 'photos/getPhotos'
        search_avatar_params = {
            'fid': input('Введите ID: '),
            'fields': 'user_photo.PIC_MAX, user_photo.LIKE_SUMMARY'
        }
        all_params = {**self.params, **search_avatar_params}
        full_params = self.get_sig(all_params)

        avatars = requests.get(search_avatar_url, params=full_params)
        sort_foto = {}
        for foto in avatars.json()['photos']:
            sort_foto[foto['like_summary']['count']] = foto['pic_max']
        return sort_foto

    def search_albums(self):
        search_avatar_url = self.url + 'photos/getAlbums'
        search_avatar_params = {
            'fid': input('Введите ID: '),
            'format': 'json'
        }
        all_params = {**self.params, **search_avatar_params}
        full_params = self.get_sig(all_params)

        avatars = requests.get(search_avatar_url, params=full_params)
        sort_albums = {}
        k = 1
        for album in avatars.json()['albums']:
            sort_albums[str(k)] = {'title':album['title'], 'aid': album['aid']}
            k += 1
        return sort_albums

    def search_foto_in_albums(self):
        sort_albums = self.search_albums()
        pprint(sort_albums)
        print(f'Введите номер альбом, фотографии которого необходимо сохранить: ')
        for album in sort_albums.keys():
            print(f"{album} - {sort_albums[album]['title']}")
        num_album = input()
        search_foto_in_albums_url = self.url + 'photos/getPhotos'
        search_foto_in_album_params = {
            'fid': '548962898298',
            'aid': sort_albums[num_album]['aid'],
            'fields': 'user_photo.PIC_MAX, user_photo.LIKE_SUMMARY, user_photo.ID',
            'count': '100'
        }
        all_params = {**self.params, **search_foto_in_album_params}
        full_params = self.get_sig(all_params)

        photos = requests.get(search_foto_in_albums_url, params=full_params)

        sort_foto = {}
        for photo in photos.json()['photos']:
            if photo['like_summary']['count'] in sort_foto:
                sort_foto[photo['id']] = photo['pic_max']
            else:
                sort_foto[photo['like_summary']['count']] = photo['pic_max']
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

# 548962898298
# user_photo:[
# ACCESS_POLICIES
# ALBUM_ID
# ANIMATED_PHOTO_SRC
# AUTHOR_REF
# BLOCKED
# BOOKMARKED
# COMMENTS_COUNT
# COMMENT_ALLOWED
# CONTEXT
# CREATED_MS
# CROP_HEIGHT
# CROP_SIZE
# CROP_WIDTH
# CROP_X
# CROP_Y
# DELETED
# DELETE_ALLOWED
# DEPTH_MAP
# DISCUSSION_SUMMARY
# HAS_FRAME
# ID
# LIKED_IT
# LIKE_ALLOWED
# LIKE_COUNT
# LIKE_SUMMARY
# MARK_ALLOWED
# MARK_AS_SPAM_ALLOWED
# MARK_AVG
# MARK_BONUS_COUNT
# MARK_COUNT
# MODERATION_STATUS
# MODIFY_ALLOWED
# OBS_SOURCE_ID
# OFFSET
# OWNER_REF
# PHOTO_ID
# PIC1024MAX
# PIC1024X768
# PIC128MAX
# PIC128X128
# PIC160X120
# PIC176X176
# PIC180MIN
# PIC190X190
# PIC240MIN
# PIC320MIN
# PIC50X50
# PIC640X480
# PICGIF
# PICMP4
# PICWEBM
# PIC_BASE
# PIC_MAX
# PINS
# PINS_CONFIRMED
# PINS_FOR_CONFIRMATION
# PIN_USERS_UNCONFIRMED
# PREVIEW_DATA
# REF
# REMOVE_FRAME
# RESHARE_SUMMARY
# ROTATION_ANGLE
# SEND_AS_GIFT_AVAILABLE
# SENSITIVE
# STANDARD_HEIGHT
# STANDARD_WIDTH
# TAG_ALLOWED
# TAG_COUNT
# TAG_COUNT_UNCONFIRMED
# TEXT
# TEXT_DETECTED
# TEXT_TOKENS
# TYPE
# USER_HAS_SEEN_PHOTO
# USER_ID
# VIEWER_MARK
# WIDGETS