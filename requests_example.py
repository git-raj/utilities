#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:08:22 2018

@author: Saroj Lamichhane
"""

import sys
import requests


#pretty print of request content
# found this handy function somewhere online

def pretty_print_req(req):
    """
    view the built request.
    This view will be slightly different than actual
    because of the way it is formatted.
    """
    print('{}\n{}\n{}\n\n{}'.format(
            '------This is the request------',
            req.method + ' '+ req.url,
            '\n'.join('{}: {}'.format(k,v) for k,v in req.headers.items()),
            req.body
            ))

## request function

def get_info():
    """
    simple get info function
    
    """

    url_google ='https://maps.googleapis.com/maps/api/geocode/json?address='+ADDRESS+'&key='+API_KEY

    req = requests.Request('GET', url_google)
    prepared = req.prepare()

    #pretty_print_req(prepared)

    #send request
    try:
        sess = requests.Session()
        message = sess.send(prepared)
        message.raise_for_status()
    except requests.exceptions.RequestException as e:
        #error, bail
        print(e)
        sys.exit(1)

    message_out = message.json()

    do_something(message_out)


#further process the message received
def do_something(message):
    print(message)


if __name__ == "__main__":
    API_KEY = 'Your_API_Key'
    ADDRESS = '1600+Amphitheatre+Parkway,+Mountain+View,+CA'
    get_info()