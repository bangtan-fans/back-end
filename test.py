import requests


payload = {"prompt": "Give me some tips to win a Hackathon."}
res = requests.post('http://localhost:5000/', json=payload)

print("response from server:",res.text)
dictFromServer = res.json()
print("\n\n\n", dictFromServer)