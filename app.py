from flask import Flask, request, jsonify, Response, make_response
import numpy
import models
from typing import List
import mlmodel
import os
from http import HTTPStatus
from typing import Union
import logging
import simplejson as json

logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello. I am app that uses word2vec!"


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
    parsed_request = req["result"]
    intent_name = parsed_request["metadata"]["intentName"]
    query = parsed_request["resolvedQuery"]

    parameters = parsed_request["parameters"]

    words = parameters["any"]

    res = mlmodel.get_words(positive=words)

    words_str = ",".join([r.word for r in res])

    speech = f"Some similar words are {words_str}"

    logging.info(f"Result is {speech}")

    return {
        "speech": speech,
        "displayText": speech,
        "source": intent_name
    }


def _parse_arguement(arg: Union[List, str]):
    if isinstance(arg, str):
        args = arg.split(",")
        args = [arg.strip() for arg in args if len(arg.strip()) > 0]
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
    negative_words = _parse_arguement(content.get("negative", None))
    num_results = content.get("size", 5)

    status_code = HTTPStatus.OK
    try:
        logging.info(f"Positive: {positive_words} , Negative: {negative_words}")
        res = mlmodel.get_words(positive=positive_words, negative=negative_words, num_words=num_results)
        payload = models.SimilarPayload(words=res)
    except Exception as e:
        status_code = HTTPStatus.BAD_REQUEST
        payload = models.ErrorPaylod(str(e))

    return Response(json.dumps(payload), mimetype=u'application/json', status=status_code)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
