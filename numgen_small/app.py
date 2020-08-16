#!flask/bin/python
from flask import Flask, jsonify, make_response
import sys
import requests
import random
import string
app = Flask(__name__)

@app.route('/numgen', methods=['GET'])
def num_gen_small():
    digits = string.digits
    rand = ''.join(random.choice(digits) for i in range(6))
    return rand

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=9019)


