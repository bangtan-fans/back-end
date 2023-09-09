import requests

url = 'http://127.0.0.1:5000/'

chat_id = "84d30410-f875-439e-9f65-67f83d57c6d2"

payload_1 = {"chat_id": chat_id,
           "prompt": "Give me three words."}

payload_2 = {"chat_id": chat_id,
           "prompt": "Concatenate them."}

x = requests.post(url, json = payload_1)

y = requests.post(url, json = payload_2)