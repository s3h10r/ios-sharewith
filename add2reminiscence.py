#!/usr/bin/env python3
"""
usage:

    add2reminiscence.py <reminiscence_instance_url> <username> <password> [<url_to_add>]

example:

    add2reminiscence.py https://apps.anypla.net/links/ guest supersecretpassword https://example.com
"""

try:
    import appex
except ImportError:
    appex = None

import getpass
import requests
import sys

__version__ = (0,1,0)
__author__ = 'sven.hessenmueller@gmail.com'
__license__ = 'MIT'

url_api = None
url2add = None
params = {'username': None, 'password': None}
headers = {}


def add_url(rem_url=None, auth_token=None, url=None, dir="/AddToReminiscence", media_link=False):
    headers = {}
    headers['Authorization'] = 'Token {}'.format(token)
    params = {'url': url, 'directory': dir, 'media_link': media_link}
    r = requests.post("{}/add-url/".format(rem_url), data=params, headers=headers) # HTTP-POST
    print(r.status_code,r.reason)
    print(r.json())
    if r.status_code != 200:
        sys.exit(-1)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        for param in params:
            if not params[param]:
                params[param] = getpass.getpass("{}?  ".format(param))
    else:
        url_api = sys.argv[1]
        if url_api[-1] != '/':
            url_api += '/'
        params['username'] = sys.argv[2]
        params['password'] = sys.argv[3]
        if len(sys.argv) > 4:
            url2add = sys.argv[4]
        else:
        	  if appex: # pythonista-instance? (e.g. on iPad/iPhone)
        	      url2add = appex.get_url()
    if not url_api:
        url_api = input('url of reminiscence instance? ')
    if not url2add:
    	  url2add = input('url to add? ')
    url_api = '{}restapi'.format(url_api)
    print("url_api : {}".format(url_api))
    print("url2add : {}".format(url2add))
    # get AUTH TOKEN
    r = requests.post("{}/login/".format(url_api), data=params, headers=headers) # HTTP-POST
    print(r.status_code,r.reason)
    print(r.json())
    token = None
    if r.status_code == 200:
        token = r.json()['token']
    else:
        sys.exit(-1)
    # add url
    if url2add:
       add_url(url_api, token, url2add)
    # logout
    r = requests.get("{}/logout/".format(url_api), params=None, headers=headers) # HTTP-GET

