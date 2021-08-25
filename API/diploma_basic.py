import requests
from tqdm import tqdm
from datetime import datetime
import json
from pprint import pprint

class YaUploader:
    def __init__(self, token_yandex: str , vk_owner_id :str ,  token_vk: str):
        self.token_yandex = token_yandex
        self.token_vk = token_vk
        self.vk_owner_id = vk_owner_id

    def upload(self, file: str , file_name : str):
        API_BASE_URL = "https://cloud-api.yandex.net/"
        headers = {
            'accept': 'application/json' ,
            'authorization': f'OAuth {self.token_yandex}'
        }
        response = requests.get(API_BASE_URL + "v1/disk", headers=headers )
        r = requests.get(API_BASE_URL + 'v1/disk/resources/upload' ,
         params={'path':'Netology/' + file_name + '.jpg'} , headers=headers , stream=True )
        try :
            upload_url = r.json()['href']
            r = requests.put(upload_url , headers=headers , files={'file' : file})
        except KeyError :
            print(f'\nFile with {file_name}.jpg  name already is on the disk')


    def profile_photos (self , count=7) :
        URL = 'https://api.vk.com/method/photos.get'
        self.file_json = list()
        params = {
         'owner_id' : self.vk_owner_id ,
         'access_token': self.token_vk ,
         'v':'5.131' ,
         'album_id' : 'profile' , 
         'extended' : '1'
        }
        res = requests.get(URL, params=params , stream=True )
        try :
            res_json = res.json()['response']
            photo = res_json['items']
            for i in tqdm(range(min(count , len(res_json['items'])))) :
                self.file_json.append(dict())
                # check same name existence and create the name
                name_exist = 0
                if (len(self.file_json) > 1) :
                    for j in range (len(self.file_json)-1) :
                        if self.file_json[j]['file_name'] in str(photo[i]['likes']['count']) :
                            self.file_json[-1]['file_name'] = (str(photo[i]['likes']['count']) + ' ' 
                            + str(datetime.utcfromtimestamp(photo[i]['date']).strftime('%Y-%m-%d ')))
                            name_exist = 1
                            break
                if name_exist != 1 :
                    self.file_json[-1]['file_name'] = str(photo[i]['likes']['count'])  
                #data of photo
                self.file_json[-1]['height'] = photo[i]['sizes'][-1]['height']
                self.file_json[-1]['width'] = photo[i]['sizes'][-1]['width']
                self.file_json[-1]['type'] = photo[i]['sizes'][-1]['type']
                self.file_json[-1]['date'] = str(photo[i]['date'])

                file = requests.get(photo[i]['sizes'][-1]['url']).content #file to upload to yandex disk
                self.upload(file , self.file_json[-1]['file_name']) # upload photo to yandex disk

        except KeyError :
            print ('Params of https://api.vk.com/method/photos.get request are incorrect')
    
    def data_to_json(self) :
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.file_json, f, ensure_ascii=False)

if __name__ == '__main__':
    token_yandex = ...
    token_vk = ...
    vk_owner_id = ...
    uploader = YaUploader(token_yandex , vk_owner_id , token_vk)
    uploader.profile_photos()
    uploader.data_to_json()


