#!flask/bin/python
from flask import Flask, jsonify, make_response, request
import sys
import requests
from random import randint
app = Flask(__name__)

@app.route('/prizegen', methods=['GET','POST'])
def prize_gen_small():
    chance = randint(0,100)
    prize = 0
    resp = "You didn't win a prize"

    if chance >= 50:
        prize = randint(1,10)
        resp = requests.get('http://notification:9000/notify').content

    payload = request.get_json(force = True)
    payload["prize"] = prize
    r = requests.post("http://db-connector:5001/account/createAccount", payload)

    return payload

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=9017)

