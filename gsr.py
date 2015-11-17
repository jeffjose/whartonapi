#!/usr/bin/python
#
# Jeffrey Jose | November 16, 2015
#
# Wharton GSR API

import sys, os
import requests
import getpass
import simplejson as json
import datetime

import auth

API = 'https://webapps.wharton.upenn.edu/whartonm/index.cfm/api/v1/'

# Wrapper around request.<httpmethod>
def req(method, url, *args, **kwargs):

    response = getattr(requests, method)(url, *args, **kwargs)

    text = json.loads(response.text)

    if 'error' in text:
        # Looks like there was an error
        raise ValueError('Error communicating with the API')

    return text, response

def api_get(endpoint, token, *args, **kwargs):    
    '''
    Wrapper for request.get
    '''
    return req('get', "%s/%s?token=%s" % (API, endpoint, token), *args, **kwargs)

def api_post(endpoint, token, *args, **kwargs):   
    '''
    Wrapper for request.post
    '''
    return req('post', "%s/%s?token=%s" % (API, endpoint, token), *args, **kwargs)

def api_put(endpoint, token, *args, **kwargs):    
    '''
    Wrapper for request.put
    '''
    return req('put', "%s/%s?token=%s" % (API, endpoint, token), *args, **kwargs)

def api_delete(endpoint, token, *args, **kwargs): 
    '''
    Wrapper for request.delete
    '''
    return req('delete', "%s/%s?token=%s" % (API, endpoint, token), *args, **kwargs)



def _parse_reservations(details):
    '''
    Massage the incoming reservation data packet
    '''

    for x in details:

        x['startTime'] = datetime.datetime.fromtimestamp(float(x['startTime']))

    return details


def get_locations(token):
    '''
    Get all the locations at Wharton. JMHH F/G/2/3 and 2401, almost always.
    '''

    locations, _ = api_get('gsr/locations', token)

    return locations

def get_reservations(token):
    '''
    Get all reservation associated with the user identified by the `token`
    '''

    details, _ = api_get('gsr/reservations', token)

    reservations = _parse_reservations(details)

    return reservations

def create_reservations(token, data):
    '''
    Create GSR Reservation for this particular user identified by the `token`

    `data` is a list of dicts of the format

    {
        'startTime'  : <timestamp>, 
        'subjectLine': <str>,
        'duration'   : (30|60|90),
        'roomId'     : <str:room_id>
        }
    '''

    # Since we're gonna modify `startTime` parameter, make a copy
    data = copy.copy(data)

    for d in data:

        d['startTime'] = time.mktime(d['startTime'].timetuple())

        text, response = api_post('gsr/reservations', token, data = d)

def delete_reservations(token, ids):
    '''
    Delete GSR Reservations with `ids` of the user (`token`)

    Takes a list of `reservationId`s
    '''

    for _id in ids:

        d = {'reservationId': _id}

        text, response = api_delete('gsr/reservations', token, data = d)

if __name__ == '__main__':

    username = raw_input('Enter your UPenn login: ')
    password = getpass.getpass('Password for %s: ' % username)

    token = auth.get_token(username, password)

    locations = get_locations(token)
    reservations = get_reservations(token)

    delete_reservations(token, [x['reservationId'] for x in reservations])
