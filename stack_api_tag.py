from pprint import pprint 
import time
import requests

current_time = int(time.time() // 1)
time_2d_ago = int((current_time - 24*60*60) // 1)

API_BASE_URI = 'https://api.stackexchange.com/questions?tagged=python&site=stackoverflow'
python_questions = requests.get(API_BASE_URI +f'&fromdate={str(time_2d_ago)}&todate={str(current_time)}')
pprint(python_questions.json())