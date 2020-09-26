import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salas-spree', methods=['POST'])
def evaluate_salad():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    n = data.get("number_of_salads");
    fff = data.get("salad_prices_street_map");
    min = 999
    result = 0
    for x in fff:
        sumw = 0
        if len(x) >= n:
            for index in range(0, len(x)-(n-1)):
                boollist = [x[lol].isdigit() for lol in range(index,index+n)]
                if False not in boollist:
                    sumw = sum([int(x[lol]) for lol in range(index,index+n)])
                    if sumw < min:
                        min = sumw
                sumw = 0
    if min == 999:
        result = 0
    else:
        result = min
    logging.info("My result :{}".format(result))
    return json.dumps(result);



