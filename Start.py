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
    dict = {'user_net': {'1': user_vk, '2': user_ok},
            '1': {'1': user_vk.photo_on_avatar, '2': user_vk.photo_on_wall, '3': user_vk.photo_in_album},
            '2': {}
            }
    print("Введите номер соответствующего пункта")
    soc_net = input("Выберите соц.сеть, в которой необходимо найти фото:\n1 - 'ВКонтакте'\n2 - 'Одноклассники'\n>>> ")
    if soc_net == '1':
        search_soc_net = input(f"Выберите место поиска фото:\n"
                               f"1 - Фото на аватаркеr\n"
                               f"2 - Фото со стены\n"
                               f"3 - Фото из альбомов\n>>> ")
    else:
        pass
    sort_foto = dict[soc_net][search_soc_net]()
    folder = user_ya.create_folder()
    user_ya.save_on_yandex_disk(sort_foto, folder)




# 185797118
# 329067411
# 85797118
# 98996500