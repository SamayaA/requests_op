import requests 
from pprint import pprint 

characters_list = ['Hulk' , 'Captain/ Amerika' , 'Thanos']
intelligence = dict()

for character in characters_list :
    r = requests.get("https://superheroapi.com/api/2619421814940190/search/" + character)
    if '/' in character :
        character_n = ''
        for word in character.split('/') :
            character_n += word
        character = character_n
    intelligence[character] = int(r.json()["results"][0]['powerstats']["intelligence"])
intelligence_max = max(intelligence)
print(intelligence_max + ' have more intelligence')