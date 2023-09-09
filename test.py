import requests

url = 'http://127.0.0.1:5000/'

chat_id = "e55e7645-7441-48ed-902a-5b8bb7a138c4"

payload_1 = {"chat_id": chat_id,
           "prompt": "Give me three words relating to academica."}

payload_2 = {"chat_id": chat_id,
           "prompt": "Now, concatenate those words."}

x = requests.post(url, json = payload_1)

y = requests.post(url, json = payload_2)