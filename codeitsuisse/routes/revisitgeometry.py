import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def evaluate_geo():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    shapecoords = data.get("shapeCoordinates");
    linecoords = data.get("lineCoordinates");
    line_grad = float(linecoords[1]["y"] - linecoords[0]["y"]) / float(linecoords[1]["x"] - linecoords[0]["x"])
    line_c = linecoords[1]["y"] - line_grad * linecoords[1]["x"]
    result = []
    for i in range(0, len(shapecoords)-1):
        for j in range(i+1, len(shapecoords)):
            minx = min([shapecoords[j]["x"], shapecoords[i]["x"]])
            maxx = max([shapecoords[j]["x"], shapecoords[i]["x"]])
            miny = min([shapecoords[j]["y"], shapecoords[i]["y"]])
            maxy = max([shapecoords[j]["y"], shapecoords[i]["y"]])
            if shapecoords[j]["y"] - shapecoords[i]["y"] == 0:
                y_val = shapecoords[j]["y"]
                x_val = (y_val - line_c)/ (line_grad)
                if isinstance(x_val, float) and x_val.is_integer():
                    x_val = int(x_val)
                if isinstance(y_val, float) and y_val.is_integer():
                    y_val = int(y_val)
                if x_val >= minx and x_val <= maxx and y_val >= miny and y_val <= maxy:
                    result.append({"x":round(x_val,2), "y":round(y_val,2)})
                
            elif shapecoords[j]["x"] - shapecoords[i]["x"] == 0:
                x_val = shapecoords[j]["x"]
                y_val = line_grad * x_val + line_c
                if isinstance(x_val, float) and x_val.is_integer():
                    x_val = int(x_val)
                if isinstance(y_val, float) and y_val.is_integer():
                    y_val = int(y_val)
                if x_val >= minx and x_val <= maxx and y_val >= miny and y_val <= maxy:
                    result.append({"x":round(x_val,2), "y":round(y_val,2)})
                
            else:
                shapeline_grad = (shapecoords[j]["y"] - shapecoords[i]["y"]) / (shapecoords[j]["x"] - shapecoords[i]["x"])
                shapeline_c = shapecoords[j]["y"] - shapeline_grad * shapecoords[j]["x"]
                x_val = (shapeline_c - line_c) / (line_grad - shapeline_grad)
                y_val = x_val * shapeline_grad + shapeline_c
                if isinstance(x_val, float) and x_val.is_integer():
                    x_val = int(x_val)
                if isinstance(y_val, float) and y_val.is_integer():
                    y_val = int(y_val)
                if x_val >= minx and x_val <= maxx and y_val >= miny and y_val <= maxy:
                    result.append({"x":round(x_val,2), "y":round(y_val,2)})
                
    logging.info("My result :{}".format(result))
    return json.dumps(result);



