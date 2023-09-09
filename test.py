import requests

url = 'http://118.138.33.86:8080/add_source_document'

chat_id = "ed8729d8-92cd-4b17-af7d-5d14b623f4cf"

payload_1 = {
    "filename": "assignment_1",
    "content": "Alex likes cats."
}


x = requests.post(url, json = payload_1)


url = 'http://118.138.33.86:8080/submit_prompt'
payload_2 = {
    "chat_id": chat_id,
    "prompt": "Tell me about what pet Alex would have and wouldn't have.",
    "source_docs": ["assignment_1"]
}

y = requests.post(url, json = payload_2)