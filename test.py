import requests

url = 'http://118.138.33.86:8080/add_source_document'

chat_id = "ed8729d8-92cd-4b17-af7d-5d14b623f4cf"

payload_1 = {
    "filename": "test_filename",
    "content": "This is a test source document file."
}


x = requests.post(url, json = payload_1)

y = requests.post(url, json = payload_2)