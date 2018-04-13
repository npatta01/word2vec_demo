from flask import Flask, request, jsonify
import numpy
import models 
from typing import List
import mlmodel
import os
from http import HTTPStatus
from typing import Union
import logging 

logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello. I am app that uses word2vec!"


def _parse_arguement(arg:Union[List,str]):
    if isinstance(arg, str):
        args = arg.split(",")
        args = [arg.strip() for arg in args if len(arg.strip())> 0]
        return args
    else:
        return arg



@app.route("/similar", methods=['GET', 'POST'])
def similar():
    if request.method == 'POST':
        content = request.json
    else:
        content = request.args

    positive_words = _parse_arguement(content["positive"])
    negative_words = _parse_arguement(content.get("negative",None))
    num_results = content.get("size", 5)        

    status_code = HTTPStatus.OK
    try:
        logging.info(f"Positive: {positive_words} , Negative: {negative_words}")
        res = mlmodel.get_words(positive=positive_words,negative=negative_words, num_words=num_results)
        payload = models.SimilarPayload(words=res)
    except Exception as e:
        status_code = HTTPStatus.BAD_REQUEST
        payload = models.ErrorPaylod(str(e))
    
    
    return jsonify(payload) , status_code  

if __name__ == "__main__":
    port = os.environ.get("PORT",5000)
    app.run(host="0.0.0.0", port=port)    