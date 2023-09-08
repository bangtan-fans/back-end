#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, jsonify
from openapi import get_completion

app = Flask(__name__)
    
@app.route('/', methods=['POST'])
def update_record():
    message_body = json.loads(request.data)
    prompt = message_body["prompt"]


    return jsonify(get_completion(prompt))


app.run(debug=True)