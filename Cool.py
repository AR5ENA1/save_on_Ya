import yandex
import vkontakte
import odnoklassniki
import json
from pprint import pprint

if __name__ == '__main__':
    with open('token_vk.txt') as file:
        token_vk = file.read()
    with open('token_ya.txt') as file:
        token_ya = file.read()
    with open("token_ok.json") as file:
        token_ok = json.load(file)
    user_vk = vkontakte.Vk(token_vk)
    user_ya = yandex.Yandex_disk(token_ya)
    user_ok = odnoklassniki.Ok(token_ok)
    # sort_foto = user_vk.foto_on_avatar()
    # folder = user_ya.create_folder()
    # user_ya.save_on_yandex_disk(sort_foto, folder)
    # sort_foto = user_vk.foto_on_wall()
    # folder = user_ya.create_folder()
    # user_ya.save_on_yandex_disk(sort_foto, folder)
    sort_foto = user_ok.search_avatar()
    pprint(sort_foto)




# 185797118
# 329067411
# 85797118
