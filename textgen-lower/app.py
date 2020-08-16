#!flask/bin/python
from flask import Flask, jsonify, make_response
import sys
import requests
import string
import random
app = Flask(__name__)

@app.route('/textgen', methods=['GET'])
def text_gen_small():
    letters = string.ascii_lowercase
    randLetters = ''.join(random.choice(letters) for i in range(2))
    return randLetters

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=9018)




