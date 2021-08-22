import requests
from datetime import datetime
import json
# импортируем pprint для более комфортного вывода информации
from pprint import pprint

class YaUploader:
    def __init__(self, token_yandex: str , token_vk: str):
        self.token_yandex = token_yandex
        self.token_vk = token_vk
        self.file_json = list()

    def upload(self, file: str , file_name : str):
        API_BASE_URL = "https://cloud-api.yandex.net/"
        headers = {
            'accept': 'application/json' ,
            'authorization': f'OAuth {self.token_yandex}'
        }
        response = requests.get(API_BASE_URL + "v1/disk", headers=headers )
        r = requests.get(API_BASE_URL + 'v1/disk/resources/upload' , params={'path':'Netology/' + file_name + '.jpg'} , headers=headers , stream=True )
        try :
            upload_url = r.json()['href']
            r = requests.put(upload_url , headers=headers , files={'file' : file})
        except KeyError :
            print(f'File with {file_name}.jpg  name already is on the disk')


    def profile_photos (self) :
        URL = 'https://api.vk.com/method/photos.get'
        params = {
         'owner_id': '560059273',
         'access_token': self.token_vk,
         'v':'5.131' ,
         'album_id' : 'profile' , 
         'extended' : '1'
        }
        res = requests.get(URL, params=params , stream=True )
        try :
            res_json = res.json()['response']
            for photo in res_json['items'] :
                self.file_json.append(dict())

                name_exist = 0
                if (len(self.file_json) != 1) :
                    for file in self.file_json :
                        if file['file_name'] in str(photo['likes']['count']) :
                            self.file_json[-1]['file_name'] = str(photo['likes']['count']) + ' ' + str(datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d '))
                            name_exist = 1
                            break
                if name_exist != 1 :
                   self.file_json[-1]['file_name'] = str(photo['likes']['count'])  

                self.file_json[-1]['height'] = photo['sizes'][-1]['height']
                self.file_json[-1]['width'] = photo['sizes'][-1]['width']
                self.file_json[-1]['type'] = photo['sizes'][-1]['type']
                self.file_json[-1]['date'] = str(photo['date'])

                file = requests.get(photo['sizes'][-1]['url']).content #file to upload to yandex disk
                self.upload(file , self.file_json[-1]['file_name']) # upload photo to yandex disk
        except KeyError :
            print ('Params of https://api.vk.com/method/photos.get request are incorrect')
    
    def data_to_json(self) :
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.file_json, f, ensure_ascii=False)

if __name__ == '__main__':
    path_to_file = 'Users/Samaya/Desktop/Netology/OOP/requests/Netology'
    token_yandex = ...
    token_vk = ...
    uploader = YaUploader(token_yandex , token_vk)
    uploader.profile_photos()
    uploader.data_to_json()


