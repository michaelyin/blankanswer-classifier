#!/usr/bin/env python

from __future__ import division, unicode_literals

import argparse
import os
import time

import onmt.model_builder
import onmt.translate
import onmt.translate.beam
from onmt.translate.translator import build_translator
from onmt.utils.logging import init_logger

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
    onmt.opts.add_md_help_argument(parser)
    onmt.opts.translate_opts(parser)

    opt = parser.parse_args()

    logger = init_logger(opt.log_file)
    translator = build_translator(opt, report_score=False)

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
        # request_id=request['id']
        res['id'] = request_id

        start_t = current_milli_time()
        img_file_path = filename  # in png format

        # preprocess image
        filename, postfix, processed_img = img_file_path, '.png', outdir + '/' + str(request_id) + '_preprocessed.png'
        crop_blank_default_size, pad_size, buckets, downsample_ratio = [600, 60], (8, 8, 8, 8), default_buckets, 2

        l = (filename, postfix, processed_img, crop_blank_default_size, pad_size, buckets, downsample_ratio)
        preprocess(l)

        # construct data
        # os.system('echo '+ str(request_id)+'_preprocessed.png ' +'>uploads/test.txt');
        os.system('echo ' + filename + '>uploads/test.txt');
        # src=  'uploads/test.txt'
        # src_dir='uploads'
        # print "src=", src
        # print "src_dir=", src_dir

        all_scores, n_best_preds = translator.translate(src=opt.src, tgt=None, src_dir=opt.src_dir,
                                                        batch_size=opt.batch_size, attn_debug=opt.attn_debug)

        now_t = current_milli_time()
        if debug:
            print "time spent ", now_t - start_t

        # process the output
        n_best_latex = []
        for pred in n_best_preds[0]:
            # print "pred:",  pred, type(pred)
            n_best_latex.append(detokenizer(''.join(pred)))

        # return the output for the api
        res['status'] = "success"
        res['info'] = now_t - start_t
        res['mathml'] = ''
        res['latex'] = n_best_latex[0]
        res['n_best_latex'] = n_best_latex
        # app.logger.debug(str(request_id)+"\t"+n_best_latex[0]+"\n");
        return_list.append(res)
        # return res

    return model_api


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


