#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.04'
__author__ = 'Liao Xuefeng (askxuefeng@gmail.com)'

'''
Python client SDK for sina weibo API using OAuth 2.
'''

try:
    import json
except ImportError:
    import simplejson as json
import time
import urllib
import urllib2
import logging

def _obj_hook(pairs):
    '''
    convert json object to python object.
    '''
    o = JsonObject()
    for k, v in pairs.iteritems():
        o[str(k)] = v
    return o

class APIError(StandardError):
    '''
    raise APIError if got failed json message.
    '''
    def __init__(self, error_code, error, request):
        self.error_code = error_code
        self.error = error
        self.request = request
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, request: %s' % (self.error_code, self.error, self.request)

class JsonObject(dict):
    '''
    general json object that can bind any fields but also act as a dict.
    '''
    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value

def _encode_params(**kw):
    '''
    Encode parameters.
    '''
    args = []
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

def _encode_multipart(**kw):
    '''
    Build a multipart/form-data body with generated random boundary.
    '''
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in kw.iteritems():
        data.append('--%s' % boundary)
        if hasattr(v, 'read'):
            # file-like object:
            ext = ''
            filename = getattr(v, 'name', '')
            n = filename.rfind('.')
            if n != (-1):
                ext = filename[n:].lower()
            content = v.read()
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Length: %d' % len(content))
            data.append('Content-Type: %s\r\n' % _guess_content_type(ext))
            data.append(content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v.encode('utf-8') if isinstance(v, unicode) else v)
    data.append('--%s--\r\n' % boundary)
    return '\r\n'.join(data), boundary

_CONTENT_TYPES = { '.png': 'image/png', '.gif': 'image/gif', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.jpe': 'image/jpeg' }

def _guess_content_type(ext):
    return _CONTENT_TYPES.get(ext, 'application/octet-stream')

_HTTP_GET = 0
_HTTP_POST = 1
_HTTP_UPLOAD = 2

def _http_get(url, authorization=None, **kw):
    logging.info('GET %s' % url)
    return _http_call(url, _HTTP_GET, authorization, **kw)

def _http_post(url, authorization=None, **kw):
    logging.info('POST %s' % url)
    return _http_call(url, _HTTP_POST, authorization, **kw)

def _http_upload(url, authorization=None, **kw):
    logging.info('MULTIPART POST %s' % url)
    return _http_call(url, _HTTP_UPLOAD, authorization, **kw)

def _http_call(url, method, authorization, **kw):
    '''
    send an http request and expect to return a json object if no error.
    '''
    params = None
    boundary = None
    if method==_HTTP_UPLOAD:
        params, boundary = _encode_multipart(**kw)
    else:
        params = _encode_params(**kw)
    http_url = '%s?%s' % (url, params) if method==_HTTP_GET else url
    http_body = None if method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)
    if authorization:
        req.add_header('Authorization', 'OAuth2 %s' % authorization)
    if boundary:
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    resp = urllib2.urlopen(req)
    body = resp.read()
    r = json.loads(body, object_hook=_obj_hook)
    if hasattr(r, 'error_code'):
        raise APIError(r.error_code, getattr(r, 'error', ''), getattr(r, 'request', ''))
    return r

class HttpObject(object):

    def __init__(self, client, method):
        self.client = client
        self.method = method

    def __getattr__(self, attr):
        def wrap(**kw):
            if self.client.is_expires():
                raise APIError('21327', 'expired_token', attr)
            return _http_call('%s%s.json' % (self.client.api_url, attr.replace('__', '/')), self.method, self.client.access_token, **kw)
        return wrap

class APIClient(object):
    '''
    API client using synchronized invocation.
    '''
    def __init__(self, app_key, app_secret, redirect_uri=None, response_type='code', domain='api.weibo.com', version='2'):
        self.client_id = app_key
        self.client_secret = app_secret
        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.auth_url = 'https://%s/oauth2/' % domain
        self.api_url = 'https://%s/%s/' % (domain, version)
        self.access_token = None
        self.expires = 0.0
        self.get = HttpObject(self, _HTTP_GET)
        self.post = HttpObject(self, _HTTP_POST)
        self.upload = HttpObject(self, _HTTP_UPLOAD)

    def set_access_token(self, access_token, expires_in=time.time()+3600):
        self.access_token = str(access_token)
        self.expires = float(expires_in)

    def get_authorize_url(self, redirect_uri=None, display='default'):
        '''
        return the authroize url that should be redirect.
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        return '%s%s?%s' % (self.auth_url, 'authorize', \
                _encode_params(client_id = self.client_id, \
                        response_type = 'code', \
                        display = display, \
                        redirect_uri = redirect))

    def request_access_token(self, code, redirect_uri=None):
        '''
        return access token as object: {"access_token":"your-access-token","expires_in":12345678}, expires_in is standard unix-epoch-time
        '''
        redirect = redirect_uri if redirect_uri else self.redirect_uri
        if not redirect:
            raise APIError('21305', 'Parameter absent: redirect_uri', 'OAuth2 request')
        r = _http_post('%s%s' % (self.auth_url, 'access_token'), \
                client_id = self.client_id, \
                client_secret = self.client_secret, \
                redirect_uri = redirect, \
                code = code, grant_type = 'authorization_code')
        r.expires_in += int(time.time())
        return r

    def is_expires(self):
        return not self.access_token or time.time() > self.expires

    def __getattr__(self, attr):
        return getattr(self.get, attr)


from tornado.auth import OAuth2Mixin
from tornado import httpclient
from tornado import escape

def callback(s):
    ''' for qq callback '''
    return s

class QQGraphMixin(OAuth2Mixin):
    """QQ authentication using the new Graph API and OAuth2."""
    _OAUTH_ACCESS_TOKEN_URL = "https://graph.qq.com/oauth2.0/token?"
    _OAUTH_AUTHORIZE_URL = "https://graph.qq.com/oauth2.0/authorize?"
    _OAUTH_NO_CALLBACKS = False
    def get_authenticated_user(self, redirect_uri, client_id, client_secret, code, callback, extra_fields=None):
        http = httpclient.AsyncHTTPClient()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "extra_params" : {"grant_type":"authorization_code"},
            }
        fields = set(['nickname', 'figureurl_2', 'gender', 'qqid'])
        if extra_fields: fields.update(extra_fields)
        http.fetch(self._oauth_request_token_url(**args), self.async_callback(self._on_access_token, redirect_uri, client_id, client_secret, callback, fields))
    
    def _on_access_token(self, redirect_uri, client_id, client_secret, callback, fields, response):
        body = response.body
        try:
            args = json.loads(body, object_hook=_obj_hook)
        except:
            if body.startswith('callback'):
                body = body.replace(';','')
                args = _obj_hook(eval(body))
            else:
                args = _obj_hook(dict([b.split('=') for b in body.split('&')]))
        if hasattr(args, 'error'):
            logging.info('QQ auth error: %s' % str(args.error_description))
            callback(None)
            return
        session = {
            "access_token": args.access_token,
            "expires": args.expires_in
        }
        self.qq_request(path="/oauth2.0/me", callback=self.async_callback(self._on_get_open_id, callback, session, fields), access_token=session["access_token"], fields=",".join(fields))
    
    def _on_get_open_id(self, callback, session, fields, reps):
        if reps is None:
            callback(None)
            return
        reps['session'] = session
        reps['fields'] = fields
        callback(reps)
    
    def _on_get_user_info(self, callback, fields, openid, user):
        if user is None:
            callback(None)
            return
        user['qqid'] = openid
        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)
        callback(fieldmap)

    def qq_request(self, path, callback, access_token=None, post_args=None, **args):
        url = "https://graph.qq.com" + path
        all_args = {}
        if access_token:
            all_args["access_token"] = access_token
            all_args.update(args)
            all_args.update(post_args or {})
        if all_args: url += "?" + urllib.urlencode(all_args)
        callback = self.async_callback(self._on_qq_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_qq_request(self, call_back, response):
        body = response.body
        body = ''.join(body.replace(';','').split())
        r = eval(body)
        if hasattr(r, 'error'):
            logging.logging("Error response %s fetching %s", r.error_description, response.request.url)
            call_back(None)
            return
        call_back(r)



class RenrenGraphMixin(OAuth2Mixin):
    """QQ authentication using the new Graph API and OAuth2."""
    _OAUTH_ACCESS_TOKEN_URL = "http://graph.renren.com/oauth/token?"
    _OAUTH_AUTHORIZE_URL = "http://graph.renren.com/oauth/authorize?"
    RENREN_SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
    RENREN_API_SERVER = "http://api.renren.com/restserver.do"
    _OAUTH_NO_CALLBACKS = False
    def get_authenticated_user(self, redirect_uri, client_id, client_secret, code, callback, extra_fields=None):
        http = httpclient.AsyncHTTPClient()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "extra_params" : {"grant_type":"authorization_code"},
            }
        fields = set(['nickname', 'figureurl_2', 'gender', 'qqid'])
        if extra_fields: fields.update(extra_fields)
        http.fetch(self._oauth_request_token_url(**args), self.async_callback(self._on_access_token, redirect_uri, client_id, client_secret, callback, fields))
    
    
    def _on_access_token(self, redirect_uri, client_id, client_secret, callback, fields, response):
        body = response.body
        try:
            args = json.loads(body, object_hook=_obj_hook)
        except:
            if body.startswith('callback'):
                body = body.replace(';','')
                args = _obj_hook(eval(body))
            else:
                args = _obj_hook(dict([b.split('=') for b in body.split('&')]))
        if hasattr(args, 'error'):
            logging.info('RenRen auth error: %s' % str(args.error_description))
            callback(None)
            return
        session_args = {"access_token": args.access_token}
        response = urllib.urlopen(RENREN_SESSION_KEY_URI + "?" + urllib.urlencode(session_args)).read()
        session_key = str(json.loads(body, object_hook=_obj_hook).renren_token["session_key"])
        
        
        self.qq_request(path="/oauth2.0/me", callback=self.async_callback(self._on_get_open_id, callback, session, fields), access_token=session["access_token"], fields=",".join(fields))
        
        
        
        '''Requesting the Renren API Server obtain the user's base info.'''
        params = {"method": "users.getInfo", "fields": "name,tinyurl"}
        api_client = RenRenAPIClient(session_key, RENREN_APP_API_KEY, RENREN_APP_SECRET_KEY)
        response = api_client.request(params);
        
        
        
        
    
    def _on_get_open_id(self, callback, session, fields, reps):
        if reps is None:
            callback(None)
            return
        reps['session'] = session
        reps['fields'] = fields
        callback(reps)
    
    def _on_get_user_info(self, callback, fields, openid, user):
        if user is None:
            callback(None)
            return
        user['qqid'] = openid
        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)
        callback(fieldmap)
    
    def renren_request(self, path, callback, access_token=None, post_args=None, **args):
        url = "http://graph.renren.com/renren_api/session_key" + path
        all_args = {}
        if access_token:
            all_args["access_token"] = access_token
            all_args.update(args)
            all_args.update(post_args or {})
        if all_args: url += "?" + urllib.urlencode(all_args)
        callback = self.async_callback(self._on_qq_request, callback)
        http = httpclient.AsyncHTTPClient()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args), callback=callback)
        else:
            http.fetch(url, callback=callback)
    
    def _on_qq_request(self, call_back, response):
        body = response.body
        body = ''.join(body.replace(';','').split())
        r = eval(body)
        if hasattr(r, 'error'):
            logging.logging("Error response %s fetching %s", r.error_description, response.request.url)
            call_back(None)
            return
        call_back(r)






class RenRenAPIClient(object):
    def __init__(self, session_key = None, api_key = None, secret_key = None):
        self.session_key = session_key
        self.api_key = api_key
        self.secret_key = secret_key
    
    def request(self, params = None):
        """Fetches the given method's response returning from RenRen API.
        Send a POST request to the given method with the given params.
        """
        params["api_key"] = self.api_key
        params["call_id"] = str(int(time.time() * 1000))
        params["format"] = "json"
        params["session_key"] = self.session_key
        params["v"] = '1.0'
        sig = self.hash_params(params);
        params["sig"] = sig
        post_data = None if params is None else urllib.urlencode(params)
        file = urllib.urlopen(RENREN_API_SERVER, post_data)
        try:
            s = file.read()
            logging.info("api response is: " + s)
            response = _parse_json(s)
        finally:
            file.close()
        if type(response) is not list and response["error_code"]:
            logging.info(response["error_msg"])
            raise RenRenAPIError(response["error_code"], response["error_msg"])
        return response
        
    def hash_params(self, params = None):
        hasher = hashlib.md5("".join(["%s=%s" % (self.unicode_encode(x), self.unicode_encode(params[x])) for x in sorted(params.keys())]))
        hasher.update(self.secret_key)
        return hasher.hexdigest()
        
    def unicode_encode(self, str):
        """
        Detect if a string is unicode and encode as utf-8 if necessary
        """
        return isinstance(str, unicode) and str.encode('utf-8') or str
    
class RenRenAPIError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code
