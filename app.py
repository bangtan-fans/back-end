#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
from openapi import OpenAIAPI
from database import Database
import uuid
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://main.d1weq6l2prlwb3.amplifyapp.com/"}})
database = Database()
openAIAPI= OpenAIAPI(database)



def generate_unique_id():
    """Generate a unique ID using UUID."""
    return str(uuid.uuid4())

@app.route('/get_all_ids', methods=['GET'])
def get_all_ids():
    return jsonify(database.get_all_ids())

@app.route('/get_all_messages/<chat_id>')
def get_all_messages(chat_id):
    return jsonify(database.get_all_messages(chat_id))

@app.route('/new_chat', methods = ['GET'])
def new_chat():
    new_chat_id = generate_unique_id()
    database.add_new_chat(chat_id = new_chat_id)
    return jsonify({"new_chat_id": new_chat_id})

@app.route('/delete_chat_id/<chat_id>', methods = ['DELETE'])
def delete_chat_id(chat_id):
    return database.delete_chat(chat_id)



@app.route('/update_document', methods = ['POST'])
def update_document():
    message_body = json.loads(request.data)
    # In production, refer to these with IDs instead.
    filename = message_body["filename"]
    content = message_body["content"]

    database.update_document(filename=filename, new_content=content)
    return "Success"




@app.route('/submit_prompt', methods=['POST'])
def submit_prompt():
    message_body = json.loads(request.data)
    chat_id = message_body["chat_id"]
    prompt = message_body["prompt"]

    #check if source docs have been selected for this chat 
    documents_list = message_body["documents_list"]
    
    response = openAIAPI.get_completion(chat_id=chat_id, prompt=prompt, documents_list = documents_list)
    return response

# Documents

@app.route('/add_document', methods = ['POST'])
def add_document():
    message_body = json.loads(request.data)
    # Assume it's in the format of "filename": "name", "content": "text"
    database.add_document(filename=message_body["filename"], content=message_body["content"], doc_type=message_body["doc_type"])
    return "Success"

@app.route('/get_document/<document_name>', methods=['GET'])
def get_document(document_name):
    """This takes a document name and returns the object stored for that document.
    """

    #get our source document from our database by using source_document_name
    return database.get_document(filename=document_name)

@app.route('/get_all_documents', methods = ['GET'])
def get_all_documents():
    return jsonify(database.get_all_documents())


@app.route('/delete_document/<document_name>', methods = ['DELETE'])
def delete_document(document_name):
    result = database.delete_document(document_name)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))