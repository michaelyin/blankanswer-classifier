# -*- coding: utf-8 -*-
import httplib, urllib, base64
import time
import requests

_maxNumRetries = 10

class TextRecognizer(object):

    def __init__(self, key, apiLink):
        self.headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': key,
        }
        self.key = key
        self.apiLink = apiLink
        self.params = {
            # Request parameters
            'handwriting': 'true',
        }

    def processRequest(self, json, data, params):

        """
        Helper function to process the request to Project Oxford

        Parameters:
        json: Used when processing images from its URL. See API Documentation
        data: Used when processing image read from disk. See API Documentation
        headers: Used to pass the key information and the data type request
        """

        retries = 0
        result = None

        while True:
            response = requests.request('post', self.apiLink, json=json, data=data, headers=self.headers, params=params)

            if response.status_code == 429:
                print("Message: %s" % (response.json()))
                if retries <= _maxNumRetries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying!')
                    break
            elif response.status_code == 202:
                result = response.headers['Operation-Location']
            else:
                print("Error code: %d" % (response.status_code))
                print("Message: %s" % (response.json()))
            break

        return result

    def process_imageUrl(self, imageUrl):
        result = None
        json = {'url': imageUrl}
        data = None
        operationLocation = self.processRequest(json, data, self.params)
        print operationLocation
        if (operationLocation != None):
            headers = {}
            headers['Ocp-Apim-Subscription-Key'] = self.key
            while True:
                time.sleep(1)
                result = self.getOCRTextResult(operationLocation)
                #print "result: ", result
                if result['status'] == 'Succeeded' or result['status'] == 'Failed':
                    break

        return result

    def show_result(self, result):
        if result is not None:
            lines = result['recognitionResult']['lines']
            print 'total lines: ', len(lines)
            for line in lines:
                print line['text']
        else:
            print 'result is None'

    def getOCRTextResult(self, operationLocation):
        """
        Helper function to get text result from operation location

        Parameters:
        operationLocation: operationLocation to get text result, See API Documentation
        headers: Used to pass the key information
        """

        retries = 0
        result = None

        while True:
            response = requests.request('get', operationLocation, json=None, data=None, headers=self.headers, params=None)
            if response.status_code == 429:
                print("Message: %s" % (response.json()))
                if retries <= _maxNumRetries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying!')
                    break
            elif response.status_code == 200:
                result = response.json()
            else:
                print("Error code: %d" % (response.status_code))
                print("Message: %s" % (response.json()))
            break

        return result

