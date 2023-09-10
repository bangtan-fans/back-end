import requests
url =  "https://back-end-5h2fkitbqa-km.a.run.app/"

res = requests.get(url + "new_chat")
new_chat_id = res.json()["new_chat_id"]

# Open assignment 1 txt and read.
file_contents = None
with open("assignment_1.txt", "r", encoding='utf-8') as file:
    # Read the entire file into a string
    file_contents = file.read()

payload = {
    "filename": "assignment_1",
    "content": file_contents
}
res = requests.post(url + "add_source_document", json = payload)
#########################
payload = {
    "chat_id": new_chat_id,
    "prompt": "What kind of food do cats like?",
    "source_docs": ["assignment_1"]
}
res = requests.post(url + "submit_prompt", json = payload)

