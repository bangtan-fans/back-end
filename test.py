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


##################### TEST SUITE 2 - 10/09/2023 - 12:38pm ####################

# add source document 

chat_id = "f52ec616-7695-4cf1-a052-aea581d74212"

payload = {
    "filename": "assignment_1",
    "content": "Alex likes cats.",
    "doc_type": "source_doc"
}

url = 'http://118.139.76.46:8080/add_document'

x = requests.post(url, json = payload)

# add central document 

payload = {
    "filename": "Nyan_cat",
    "content": "Nyan Cat is a cat.",
    "doc_type": "central_doc"
}

url = 'http://118.139.76.46:8080/add_document'
x = requests.post(url, json = payload)


# get document (testing Nyan_cat doc we just uploaded above)

url = 'http://118.139.76.46:8080/get_document/Nyan_cat'
a = requests.get(url)

# get all documents 

url = 'http://118.139.76.46:8080/get_all_documents'
a = requests.get(url)

# delete document - 
url = 'http://118.139.76.46:8080/delete_document/assignment_1'
a = requests.delete(url)


# test update doc (save button)
import requests
url = "http://118.139.76.46:8080/update_document"

payload = {
    'filename': 'Nyan_cat',
    "content": "UPDATED CONTENT"
}

a = requests.post(url, json = payload)

# add a source doc that expands on nyan cat 
payload = {
    "filename": "nyan_cat_info",
    "content": "Nyan cat is pink. Alex likes nyan cat.",
    "doc_type": "source_doc"
}

url = 'http://118.139.76.46:8080/add_document'

x = requests.post(url, json = payload)


# test submit prompt which will now be referencing source docs and central docs 
import requests 
url = "http://118.139.76.46:8080/submit_prompt"

payload = {
    'chat_id' : '20fd9382-1108-4a4a-b08c-2db81b3e61bd',
    'prompt': 'Can you edit my central document to give more information about nyan cat?',
    "documents_list": []
}

a = requests.post(url, json = payload)

# test delete chat 

url = 'http://118.139.76.46:8080/delete_chat_id/20fd9382-1108-4a4a-b08c-2db81b3e61bd'
a = requests.delete(url)
