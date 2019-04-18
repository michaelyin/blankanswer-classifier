#!/usr/bin/env python

from __future__ import division, unicode_literals

import argparse
import os
import time
import cv2

from net.wyun.blankanswer import image_utils

default_buckets = '[[240,100], [320,80], [400,80],[400,100], [480,80], [480,100], [560,80], [560,100], [640,80],[640,100],\
 [720,80], [720,100], [720,120], [720, 200], [800,100],[800,320], [1000,200]]'
outdir = 'uploads'
debug = True

current_milli_time = lambda: int(round(time.time() * 1000))

headers = {'content-type': 'application/json'}

from flask import Flask

app = Flask(__name__)


def get_model_api():
    """Returns lambda function for api"""

    # initialize config for translate
    parser = argparse.ArgumentParser(description='translate.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    opt = parser.parse_args()


    def model_api(request_id, filename, return_list):
        """
        Args:
            input_data: submitted to the API, json string

        Returns:
            output_data: after some transformation, to be
                returned to the API

        """

        # process input

        res = {}
        # request_id=str(uuid.uuid4())
        res['id'] = request_id

        start_t = current_milli_time()
        img_file_path = filename  # in png format

        # preprocess image
        # os.system('echo '+ str(request_id)+'_preprocessed.png ' +'>uploads/test.txt');
        os.system('echo ' + filename + '>uploads/test.txt');
        print filename
        # src=  'uploads/test.txt'
        # src_dir='uploads'
        # print "src=", src
        # print "src_dir=", src_dir

        #all_scores, n_best_preds = translator.translate(src=opt.src, tgt=None, src_dir=opt.src_dir,
        #                                                batch_size=opt.batch_size, attn_debug=opt.attn_debug)

        # hasAnswer: 1 means that there is answer in image; 0 means not
        hasAnswer = 0

        now_t = current_milli_time()
        (isSuccess, hasAnswer, errmsg) = has_answer(filename)

        if debug:
            print "time spent ", now_t - start_t

        # return the output for the api
        if isSuccess:
            has_an_answer = 0
            if hasAnswer:
                has_an_answer = 1

            res['status'] = "success"
            res['info'] = now_t - start_t
            res['has_answer'] = has_an_answer
        else:
            res['status'] = "error"
            res['info'] = errmsg
            res['has_answer'] = 2
        return_list.append(res)
        # return res

    return model_api


Threshold = 1.55e-05
def has_answer(imagePath):
    '''

    :param imagePath: path of the image file being uploaded from client
    :return: (success, has_answer, errmsg)
    '''
    image = cv2.imread(imagePath)
    height, width, depth = image.shape
    if height < 45 or width < 45 or height > 1000 or width > 1000:
        return (False, False, "image size should be (45, 45) to (1000, 1000)")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU)
    mask_inv = cv2.bitwise_not(th)

    # calculate moments of binary image
    M = cv2.moments(mask_inv)
    # print M

    # calculate x,y coordinate of center
    if M["m00"] == 0:
        print "m00 is 0", imagePath
        return (False, False, "m00 is 0, bad format image!")

    #cX = int(M["m10"] / M["m00"])
    #cY = int(M["m01"] / M["m00"])

    nu02 = M["nu02"]
    print "nu02", nu02
    hasAnswer = True
    if nu02 < Threshold:
        hasAnswer = False
    return (True, hasAnswer, "")


def preprocess(l):
    filename, postfix, output_filename, crop_blank_default_size, pad_size, buckets, downsample_ratio = l
    postfix_length = len(postfix)

    try:
        im1 = image_utils.crop_image(filename, output_filename, crop_blank_default_size)
        im2 = image_utils.pad_image(im1, output_filename, pad_size, buckets)

        status = image_utils.downsample_image(im2, output_filename, downsample_ratio)
        im1.close()
        im2.close()
        return True
    except IOError:
        app.logger.info("IOError in preprocesing")
        return False


def detokenizer(s):
    s = s.replace("\left{", "{")
    s = s.replace("\left\(", "\(")
    s = s.replace("\left[", "[")
    s = s.replace("\right}", "}")
    s = s.replace("\right\)", "\)")
    s = s.replace("\right]", "]")
    s = s.rstrip()
    s = s.lstrip()
    s2 = ""
    for i, c in enumerate(s):
        if c == " " and ('0' <= s[i - 1] <= '9' or s[i - 1] == '.'):
            if s[i + 1].isalpha() or '0' <= s[i + 1] <= '9' or s[i + 1] == '.':
                continue
        s2 += c
    return s2


