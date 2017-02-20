var request = require('superagent');
var deferred = require('deferred');

var URLS = {
        'auth'     : 'https://ca-cf10.wharton.upenn.edu/authentication/',
        'ref_login': 'https://ca-cf10.wharton.upenn.edu/authentication/pennkey-secured/?service=WhartonConnectMobile',
        'login'    : 'https://weblogin.pennkey.upenn.edu/login',
        }

var _get_token = function(username, password) {

    var def = deferred()

     request.get(URLS.auth).end(function (err, response) {
        var set_cookie = response.headers['set-cookie'][0];

        var cosign = set_cookie.match(/(cosign\S*).*/)[1];

        var login_data = {
            required : 'UPENN.EDU',
            ref      : URLS.ref_login,
            service  : 'cosign-wharton-cacf10-0',
            login    : username,
            password : password
        }

        _send_login_info(login_data, cosign, def);

    })

    return def.promise;

}


var _send_login_info = function (login_data, cosign, def) {

    request.post(URLS.login)
        .set('Cookie', cosign)
        .type('form')
        .send(login_data)
        .redirects(0)
        .end(function(err, response) {

            cookies = response.headers['set-cookie']

            if (!response.headers.location) {
                def.reject(err);
                return
            }

            request.get(response.headers.location)
                .set('Cookie', cookies)
                .redirects(0)
                .end(function(err, response) {

                    cookies = response.headers['set-cookie']

                    if (!cookies) {
                        def.reject(err);
                        return
                    }

                    request.get(response.headers.location)
                        .set('Cookie', cookies)
                        .redirects(0)
                        .end(function(err, response) {

                            token =  _parse_token(response.headers.location)

                            def.resolve(token)
                        })

                })
        })
}

var _parse_token = function(location) {

    token = location.match(/.*token=(\S*)/)[1];
    return token
}

var get_token = function(username, password) {

    var def = deferred()

    _get_token(username, password)
        .then(function(res){

            def.resolve(res);

        },
        function(e){
            var e = new Error('Login unsuccessful');
            def.reject(e);
        })

    return def.promise

}

var auth = function(username, password) {

    var def = deferred()

    get_token(username, password).then(function (){

        def.resolve(true);
    }, function() {

        def.resolve(false);
    })

    return def.promise()

}

exports.auth = auth
