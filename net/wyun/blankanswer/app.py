import os
import sys
import logging
import multiprocessing
import time

from flask import Flask, request, jsonify
from flask_cors import CORS

import io
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

from serve import get_model_api


# define the app
app = Flask(__name__)
CORS(app) # needed for cross-domain requests, allow everything by default


UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# global
#global timeout_secs
#timeout_secs = 3

# load the model
model_api = get_model_api()


# API route
@app.route('/print/mathreco', methods=['POST'])
def mathreco():
    """API function

    All model-specific logic to be defined in the get_model_api()
    function
    """
    try:
        request_id=request.form['id']
    except:
        request_id=888
     
    try:
        color_space=request.form['color']
    except:
        color_space='sRGB'

    file = request.files['image']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    app.logger.debug("api_input: " + filename)

    if color_space !=  'sRGB':
        img = cv2.imread(filename)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = np.zeros_like(img)
        img2[:,:,0] = gray
        img2[:,:,1] = gray
        img2[:,:,2] = gray
        cv2.imwrite(filename, img2)
        app.logger.debug("color space converted : " + filename)

    manager = multiprocessing.Manager()
    return_list = manager.list()
    p = multiprocessing.Process(target=model_api, args=(request_id, filename,return_list))
    p.start()

    for _ in range(20*timeout_secs):
    # check worker every 50 ms 
        time.sleep(0.05)
        if len(return_list) >  0 :
            output_data =return_list[0]
            #app.logger.debug("api_output: " + str(output_data))
            # Cleanup
            p.terminate()
            p.join()
            response = jsonify(output_data)
            return response

    #output_data = model_api(input_data, return_dict)
    # Terminate worker after timeout
    app.logger.debug("Timeout")
    p.terminate()
    output_data={}
    output_data['status']='Timeout'
    output_data['info']=1000*timeout_secs
    response = jsonify(output_data)
    return response


@app.route('/')
def index():
    return "Index API"

# HTTP Errors handlers
@app.errorhandler(404)
def url_error(e):
    return """
    Wrong URL!
    <pre>{}</pre>""".format(e), 404


@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    global timeout_secs
    try:
        timeout_secs = int(os.environ["TIMEOUT_SECS"])
        app.logger.info("timout "+str(timeout_secs))
    except:
        timeout_secs=3
        app.logger.info("default timout "+str(timeout_secs))
    try:
        mathreco_port=int(os.environ["MATHRECO_PORT"])
        app.logger.info("port "+str(mathreco_port))
    except:
        mathreco_port=8080;
        app.logger.info("default port 8080")
    # This is used when running locally.
    app.run(host='0.0.0.0',port=mathreco_port, debug=True)
