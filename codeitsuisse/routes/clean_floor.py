import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluate_cf():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    tt = data.get("tests");
    ansdict = {}
    result = {}
    for index, t in enumerate(tt.values()):
        floor = t["floor"]
        counter = 0
        i = 0
        zerolist = [0]*(len(floor))
        while floor != zerolist:
            if i == 0:
                counter += 1
                i += 1
            elif i == len(floor) - 1:
                counter += 1
                i -= 1
            else:
                if floor[i-1] > 0:
                    counter += 1
                    i -= 1
                elif floor[i+1] > 0:
                    counter += 1
                    i += 1
            if floor[i] == 0:
                floor[i] += 1
            else:
                floor[i] -= 1
        ansdict[str(index)] = counter
        counter = 0
    result["answers"] = ansdict
    logging.info("My result :{}".format(result))
    return json.dumps(result);



