from flask import Flask, request, jsonify
import numpy
import models 
from typing import List
import mlmodel
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello. I am app that uses word2vec!"


@app.route("/similar", methods=['GET', 'POST'])
def similar():
    if request.method == 'POST':
        content = request.json
    else:
        content = request.args

    positive_words = content["positive"]
    negative_words = content.get("negative",None)
    num_results = content.get("size", 5)        

    res = mlmodel.get_words(positive=positive_words,negative=negative_words, num_words=num_results)
    
    paylod = models.SimilarPayload(words=res)
    return jsonify(paylod)    

if __name__ == "__main__":
    port = os.env.get(PORT,80)
    app.run(host="0.0.0.0", port=)    