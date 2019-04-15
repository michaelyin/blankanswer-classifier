# -*- coding: utf-8 -*-
import time
import urllib
from unittest import TestCase

import requests

from net.wyun.blankanswer import reco_config
from net.wyun.blankanswer import text_recognizer as reco

'''
python -m unittest net.test.wyun.blank.test_hw_answer.TestRecoText.test_reco_batch
'''
_url = reco_config._url
_key = reco_config._key

_imageBaseUrl = 'http://72.93.93.62:8000/'

class TestRecoText(TestCase):
    def setUp(self):
        self.recognizer = reco.TextRecognizer(_key, _url)

#westus.api.cognitive.microsoft.com, # "050201000101_b.jpg",

    def test_reco_text(self):
        try:
            image_url = _imageBaseUrl + '02260548.jpg'
            self.recognizer.process_imageUrl(image_url)
        except Exception as e:
            print("[Errno {0}] {1}".format(e, e))

    def test_reco_batch(self):
        img_list = ["02260148.jpg", "02260216.jpg", "02260548.jpg", \
                    "02260725.jpg", "02261236.jpg", "02261446.jpg", \
                    "02261451.jpg", "02262165.jpg", "02262249.jpg", \
                    "02262364.jpg", "02262393.jpg", "02262424.jpg", \
                    "02262719.jpg", "0226hr.jpg", \
                    "0541tu.jpg", "0990alb.jpg", "1086aot.jpg"]

        try:
            for image in img_list:
                print 'processing ' + image
                image_url = _imageBaseUrl + image
                result = self.recognizer.process_imageUrl(image_url)
                if result is not None:
                    lines = result['recognitionResult']['lines']
                    print image, ', total lines: ', len(lines)
                    for line in lines:
                        print line['text']

        except Exception as e:
            print("[Errno {0}] {1}".format(e, e))



