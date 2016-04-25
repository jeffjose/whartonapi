# whartonapi

An API ([python](#python), [javascript](#javascript)) to interact with Wharton Webservices. 

## Python
### Authentication - auth.py

##### `auth(username, password)`

```sh
>>> auth(username, password)
```

###### `get_token(username, password)`

```sh
>>> get_token(username, password)
ABCDEFGHIJK123456
```

### Group Study Rooms - gsr.py

##### `get_locations(token)`

```sh
>>> get_locations(token)
[u'JMHH F', u'JMHH G', u'JMHH 2', u'JMHH 3', u'2401']
```

##### `get_reservations(token)`

```sh
>>> get_reservations(token)
[
  {
    u'duration': 30, 
    u'reservationId': 1536217, 
    u'roomId': u'2401 813', 
    u'subjectLine': u'GSR Reservation', 
    u'startTime': datetime.datetime(2015, 11, 17, 10, 0)
   }
]
```

##### `create_reservations(token)`

```sh
>>> data = [{
    u'duration': 30, 
    u'roomId': u'2401 813', 
    u'subjectLine': u'GSR Reservation', 
    u'startTime': datetime.datetime(2015, 11, 17, 11, 0)
   }]
>>> create_reservations(token, data)
>>>
```

##### `delete_reservations(token)`

```sh
>>> reservation_ids = ['1536217']
>>> create_reservations(token, reservation_ids)
>>>
```

## Javascript
