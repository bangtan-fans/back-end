import requests

url = 'http://127.0.0.1:5000/'

url_cloudrun = "https://back-end-5h2fkitbqa-km.a.run.app"

chat_id = "dce507a8-3eda-45b1-a974-fb8636d9dd16"

payload_1 = {"chat_id": chat_id,
           "prompt": "Give me three words relating to flowers."}

payload_2 = {"chat_id": chat_id,
           "prompt": "Now, concatenate those words."}

x = requests.post(url_cloudrun, json = payload_1)

y = requests.post(url, json = payload_2)