import requests
from tqdm import tqdm
from datetime import datetime
import json
from pprint import pprint

class vk_api:
    API_BASE_URL = 'https://api.vk.com/method'
    def __init__(self, vk_owner_id :str ,  token_vk: str ) :
        self.token_vk = token_vk
        self.vk_owner_id = vk_owner_id

    def name_existance (self , existing_names , name):
        if len(existing_names) == 0 :
            return False
        if type(existing_names[0]) is str :
            for j in range (len(existing_names)) :
                if (existing_names[j] == name) :
                    return True
        elif type(existing_names[0]) is dict :
            for j in range (len(existing_names)) :
                if (existing_names[j]['file_name'] == name) :
                    return True
        return False

    def get_photo_information (self , count=7) :
        self.file_json = list()
        params = {
            'owner_id' : self.vk_owner_id ,
            'access_token': self.token_vk ,
            'v':'5.131' ,
            'album_id' : 'profile' , 
            'extended' : '1'
        }
        res = requests.get(self.API_BASE_URL + '/photos.get', params=params , stream=True )
        try :
            photos = res.json()['response']['items']
            for i in range(min(count , len(photos))) :
                if self.name_existance(self.file_json , str(photos[i]['likes']['count'])) :
                    self.file_json.append(dict())
                    self.file_json[-1]['file_name'] = (str(photos[i]['likes']['count']) + ' ' 
                            + str(datetime.utcfromtimestamp(photos[i]['date']).strftime('%Y-%m-%d ')))        
                else :
                    self.file_json.append(dict())
                    self.file_json[-1]['file_name'] = str(photos[i]['likes']['count'])  
                self.file_json[-1]['height'] = photos[i]['sizes'][-1]['height']
                self.file_json[-1]['width'] = photos[i]['sizes'][-1]['width']
                self.file_json[-1]['type'] = photos[i]['sizes'][-1]['type']
                self.file_json[-1]['date'] = str(photos[i]['date'])
        except KeyError :
            print ('Params of https://api.vk.com/method/photos.get request are incorrect')



    def photos_to_yandexd (self , yandex , count=7) :
        photo_names = list()
        params = {
         'owner_id' : self.vk_owner_id ,
         'access_token': self.token_vk ,
         'v':'5.131' ,
         'album_id' : 'profile' , 
         'extended' : '1'
        }
        res = requests.get(self.API_BASE_URL + '/photos.get', params=params , stream=True )
        try :
            photos = res.json()['response']['items']
            for i in range(min(count , len(photos))) :
                if self.name_existance(photo_names , str(photos[i]['likes']['count'])) :
                        name = (str(photos[i]['likes']['count']) + ' ' 
                            + str(datetime.utcfromtimestamp(photos[i]['date']).strftime('%Y-%m-%d ')))
                        photo_names.append(name)
                else :
                    photo_names.append(str(photos[i]['likes']['count'])) 
                file = requests.get(photos[i]['sizes'][-1]['url']).content #file to upload to yandex disk
                yandex.upload(file , photo_names[-1]) # upload photo to yandex disk

        except KeyError :
            print ('Params of https://api.vk.com/method/photos.get request are incorrect')
    
    def data_to_json(self) :
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(self.file_json, f, ensure_ascii=False)





class YaUploader:
    API_BASE_URL = "https://cloud-api.yandex.net/"
    
    def __init__(self, token_yandex: str):
        self.token_yandex = token_yandex

    def upload(self, file: str , file_name : str):
        headers = {
            'accept': 'application/json' ,
            'authorization': f'OAuth {self.token_yandex}'
        }
        response = requests.get(self.API_BASE_URL + "v1/disk", headers=headers )
        r = requests.get(self.API_BASE_URL + 'v1/disk/resources/upload' ,
         params={'path':'Netology/' + file_name + '.jpg'} , headers=headers , stream=True )
        try :
            upload_url = r.json()['href']
            r = requests.put(upload_url , headers=headers , files={'file' : file})
        except KeyError :
            print(f'\nFile with {file_name}.jpg  name already is on the disk')


    
if __name__ == '__main__':
    token_yandex = ...
    token_vk = ...
    vk_owner_id = ...
    count = 5
    uploader = YaUploader(token_yandex)
    vk = vk_api(vk_owner_id , token_vk)
    vk.photos_to_yandexd(uploader , count)
    vk.get_photo_information(count)
    vk.data_to_json()


