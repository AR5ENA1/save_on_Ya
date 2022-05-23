import yandex
import vkontakte
import odnoklassniki
import json

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
    dict = {'1': {'1': user_vk.photo_on_avatar, '2': user_vk.photo_on_wall, '3': user_vk.photo_in_album},
            '2': {'1': user_ok.search_avatar, '2': user_ok.search_photo_in_albums}
            }
    print("Введите номер соответствующего пункта")
    soc_net = input("Выберите соц.сеть, в которой необходимо найти фото:\n1 - 'ВКонтакте'\n2 - 'Одноклассники'\n>>> ")
    if soc_net == '1':
        search_soc_net = input(
            f"Выберите место поиска фото:\n"
            f"1 - Фото на аватарке\n"
            f"2 - Фото со стены\n"
            f"3 - Фото из альбомов\n>>> "
        )
    elif soc_net == '2':
        search_soc_net = input(
            f"Выберите место поиска фото:\n"
            f"1 - Фото на аватарке\n"
            f"2 - Фото из альбомов\n>>> "
        )
    id = input('Введите ID: ')
    sort_photo = dict[soc_net][search_soc_net](id)
    folder = user_ya.create_folder()
    user_ya.save_on_yandex_disk(sort_photo, folder)
    user_ya.save_in_json(folder)
