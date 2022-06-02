import yandex
import vkontakte
import odnoklassniki
import json
import configparser


def search_foto_vk():
    search_soc_net = input(
        f"Выберите место поиска фото:\n"
        f"1 - Фото на аватарке\n"
        f"2 - Фото со стены\n"
        f"3 - Фото из альбомов\n>>> "
    )
    if search_soc_net in ('1', '2', '3'):
        return search_soc_net
    else:
        print('Вы ввели недопустимое значение!')
        search_foto_vk()


def search_foto_ok():
    search_soc_net = input(
        f"Выберите место поиска фото:\n"
        f"1 - Фото на аватарке\n"
        f"2 - Фото из альбомов\n>>> "
    )
    if search_soc_net in ('1', '2'):
        return search_soc_net
    else:
        print('Вы ввели недопустимое значение!')
        search_foto_ok()


def search_foto(user_vk, user_ya):
    print("Введите номер соответствующего пункта")
    soc_net = input("Выберите соц.сеть, в которой необходимо найти фото:\n1 - 'ВКонтакте'\n2 - 'Одноклассники'\n>>> ")
    if soc_net == '1':
        search_soc_net = search_foto_vk()
    elif soc_net == '2':
        search_soc_net = search_foto_ok()
    else:
        print('Неверный выбор!')
        search_foto(user_vk, user_ya)
    profile = input('Введите ID: ')
    sort_photo = command[soc_net][search_soc_net](profile)
    return sort_photo


def count_foto(sort_photo):
    count = input('Введите количество фотографий которое необходимо сохранить: ')
    try:
        int(count)
    except ValueError:
        print('Введено некорректное значение!')
        count_foto(sort_photo)
    else:
        if int(count) > 0:
            photos = {}
            for x,y in list(sort_photo.items())[:int(count)]:
                    photos[x] = y
            return photos
        else:
            print('Введено некорректное значение!')
            count_foto(sort_photo)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("token.ini")
    user_vk = vkontakte.Vk(config["vkontakte"]["token"])
    user_ya = yandex.Yandex_disk(config["yandex_disk"]["token"])
    user_ok = odnoklassniki.Ok(dict(config["odnoklassniki"]))

    command = {'1': {'1': user_vk.photo_on_avatar, '2': user_vk.photo_on_wall, '3': user_vk.photo_in_album},
               '2': {'1': user_ok.search_avatar, '2': user_ok.search_photo_in_albums}
               }

    sort_photo = search_foto(user_vk, user_ya)
    photos = count_foto(sort_photo)
    folder = user_ya.create_folder()
    user_ya.save_on_yandex_disk(photos, folder)
    user_ya.save_in_json(folder)
