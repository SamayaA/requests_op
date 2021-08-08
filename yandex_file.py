import requests
# from pprint import pprint

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        API_BASE_URL = "https://cloud-api.yandex.net/"
        headers = {
            'accept': 'application/json' ,
            'authorization': f'OAuth {self.token}'
        }
        
        response = requests.get(API_BASE_URL + "v1/disk", headers=headers )
        r = requests.get(API_BASE_URL + 'v1/disk/resources/upload' , params={'path':'Netology/data.txt'} , headers=headers )
        upload_url = r.json()['href']
        r = requests.put(upload_url , headers=headers , files={'file' :open('data.txt' , 'r')})


if __name__ == '__main__':
    path_to_file = 'Users/Samaya/Desktop/Netology/OOP/requests/Netology'
    token = ...
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
