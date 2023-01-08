import requests
import json
from pprint import pprint


class VK:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photo(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id, 'album_id': 'profile', 'extended': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


def get_token_vk():
    with open("token_vk.txt", "r") as file:
        return file.readline()


user_id = '17478390'
vk = VK(get_token_vk(), user_id)
photo_info = vk.get_photo()


def get_photo_url():
    photo_unit = 0
    url_list = []
    for photo_unit in range(len(photo_info['response']['items'])):
        path = photo_info['response']['items'][photo_unit]
        url_list.append(path['sizes'][-1]['url'])
        photo_unit += 1
    return url_list


def get_photo_info():
    likes_and_size_photo = []
    for photo_unit in range(len(photo_info['response']['items'])):
        path = photo_info['response']['items'][photo_unit]
        size_type = path['sizes'][-1]['type']
        likes = path['likes']['count']
        photo_unit += 1
        likes_and_size_photo.append({'name': likes, 'size': size_type})
    with open('data.json', 'w') as write_file:
        json.dump(likes_and_size_photo, write_file)


photo_url_list = get_photo_url()


class YaUploader:
    files_url = "https://cloud-api.yandex.net/v1/disk/resources/files"
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"

    def __init__(self, token: str):
        self.token = token

    @property
    def headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"OAuth {self.token}"
        }

    def upload(self):
        with open("data.json", "r") as read_file:
            to_json = json.load(read_file)
            for n in range(len(to_json)):
                x = to_json[n]['name']
                path = f"disk/New/{x}.jpg"
                params = {"url": i, "path": path}
                response = requests.post(self.upload_url, params=params)
                if response.status_code == 201:
                    print("Файл загружен")
                    return True
                print("Файл не загружен, потому что", response.status_code)
                return False


def get_token_ya():
    with open("token_ya.txt", "r") as file:
        return file.readline()


ya_client = YaUploader(get_token_ya())
for photo_url in photo_url_list:
    ya_client.upload(photo_url)

pprint(get_photo_info())
