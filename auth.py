#!/usr/bin/python
#
# Jeffrey Jose | November 16, 2015
#
# UPenn/Wharton Authentication

import sys, os
import re
import requests
import getpass

URLS = {
        'auth'     : 'https://ca-cf10.wharton.upenn.edu/authentication/',
        'ref_login': 'https://ca-cf10.wharton.upenn.edu/authentication/pennkey-secured/?service=WhartonConnectMobile',
        'login'    : 'https://weblogin.pennkey.upenn.edu/login',
        }

def _get_cookie(header, name):
    '''
    Get cookie string from the header. `name` is not matched exactly
    '''

    return re.search('%s\S+' % name, header).group()

def _make_headers(header_strings):
    '''
    Make key:value pairs from the header_strings
    '''

    headers = {}

    for header_string in header_strings:

        key, val = header_string.split('=')

        headers[key] = val

    return headers

def _parse_token(url):

    return re.search('token=(\S+)', url).groups()[0]


def _get_token(username, password, urls = URLS):
    '''
    Authenticates using wharton/upenn resource and returns the token
    '''

    # Step 1
    #
    response = requests.get(urls['auth'])

    # Get Host Cookie from the first location it hits (response.history[0])
    #hostCookie = _get_cookie(response.history[0].headers['Set-Cookie'], 'BIGipServer') 

    # Get Hash Cookie from the final location (response)
    hashCookie = _get_cookie(response.headers['Set-Cookie'], 'cosign')


    # Step 2
    #
    loginData = {
            'required' : 'UPENN.EDU',
            'ref'      : urls['ref_login'],
            'service'  : 'cosign-wharton-cacf10-0',
            'login'    : username,
            'password' : password
            }

    loginCookies = _make_headers([hashCookie])

    response = requests.post(urls['login'], data = loginData, cookies = loginCookies)

    finalURL = response.url

    token = _parse_token(finalURL)

    return token

def auth(username, password, urls = URLS):
    '''
    Authenticates username/password combination. 

    Raises ValueError() if the credentials are incorrect
    '''

    try:
        token = get_token(username, password, urls)
    except:
        raise ValueError("Login unsuccessful")
    finally:
        return True

def get_token(username, password, urls = URLS):
    '''
    Authenticates using wharton/upenn resource and returns the token
    '''

    try:
        token = _get_token(username, password, urls = URLS)
    except:
        raise ValueError('Login unsuccessful')
    else:
        return token

if __name__ == '__main__':

    username = raw_input('Enter your UPenn login: ')
    password = getpass.getpass('Password for %s: ' % username)

    auth(username, password)
