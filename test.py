import requests

url = 'http://118.139.76.46:8080/add_source_document'

chat_id = "ed8729d8-92cd-4b17-af7d-5d14b623f4cf"

payload_1 = {
    "filename": "assignment_1",
    "content": "Alex likes cats.",
    "doc_type": "source_doc"
}


x = requests.post(url, json = payload_1)


url = 'http://118.138.33.86:8080/submit_prompt'
payload_2 = {
    "chat_id": chat_id,
    "prompt": "Tell me about what pet Alex would have and wouldn't have.",
    "source_docs": ["assignment_1"]
}

y = requests.post(url, json = payload_2)

#deleting a chat 
url = 'http://118.138.33.86:8080/delete_chat_id'
chat_id = "1064d9fa-0820-4c24-9cd0-336687209e4d"
payload_3 = {
    "chat_id": chat_id,
}

z = requests.delete(url, json = payload_3)

#deleting a source document
url = 'http://118.138.33.86:8080/delete_source_document'
document_name = "assignment_1"
payload_4 = {
    "source_document_name": document_name,
}

z = requests.delete(url, json = payload_4)

url = "http://118.139.76.46:8080/add_source_document"