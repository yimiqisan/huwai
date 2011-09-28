#!/usr/bin/env python
# encoding: utf-8
"""
tools.py

Created by 刘 智勇 on 2011-09-24.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
#!/usr/bin/env python
# encoding: utf-8
"""
tools.py

Created by 刘 智勇 on 2011-08-15.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import logging
import redis
import cPickle as pickle
from datetime import datetime, timedelta
import uuid
import functools
from base64 import urlsafe_b64encode, urlsafe_b64decode

from huwai.config import DB_CON, DB_NAME, SESSION_SET


class SessionManager(object):
    """
    Session manager class, used to manage the various session objects and talk with Redis.
    """

    class _instance_():
        def __init__(self, session_expire_time=SESSION_SET["SESSION_EXPIRE_TIME"], redis_url=SESSION_SET["REDIS_URL"], on_delete=None):
            self._rd = redis.Redis(host=redis_url['ip'], port=redis_url['port'], db=redis_url['db'])
            self._on_delete = on_delete
            self._session_expire_time = session_expire_time

        def get_session(self, cookie=None):
            try:
                data = self._rd.get(cookie)
                session = pickle.loads(data)
                if session.is_expired:
                    self.delete_session(session)
                    raise Exception
                else:
                    session.renew()
            except Exception, e:
                session = Session(self._session_expire_time)
            return session

        def get_all_sessions(self):
            for sid in self._rd.keys('*'):
                session = self._rd.get(sid)
                session = pickle.loads(session)
                yield session

        def save_session(self, session):
            data = pickle.dumps(session)
            return self._rd.set(session.sid, data)

        def delete_session(self, session):
            if self._on_delete:
                self._on_delete(session.sid)
            return self._rd.delete(session.sid)
            
        def test(self):
            return self._on_delete

    instance = {}
    def __init__(self, *args):
        if self.__class__ not in SessionManager.instance:
            SessionManager.instance[self.__class__] = SessionManager._instance_(*args)
        else:
            return None

    def __getattr__(self, name):
        return getattr(self.instance[self.__class__], name)

    def __setattr__(self, name, value):
        return setattr(self.instance[self.__class__], name, value)


class Session(object):
    """
    Session object, works like a dict.
    """

    def __init__(self, session_expire):
        self.sid = self._generate_sid()
        self._expires_in = timedelta(seconds=session_expire)
        self._last_update = datetime.now()
        self.data = dict()

    def _generate_sid(self):
        return uuid.uuid4().hex

    @property
    def is_expired(self):
         td = datetime.now() - self._last_update
         return td > self._expires_in

    def get(self, key, value=None):
        try:
            ret = self.data[key]
        except:
            return value
        return ret

    def renew(self):
        self._last_update = datetime.now()
        self.save()

    def has_key(self, keyname):
        return self.__contains__(keyname)

    def save(self):
        return SessionManager().save_session(self)

    def delete(self):
        return SessionManager().delete_session(self)

    def __delitem__(self, key):
        del self.data[key]
        self.save()
        return True

    def __getitem__(self, key):
        try:
            value = self.data[key]
        except:
            value = None
        return value

    def __setitem__(self, key, val):
        self.data[key] = val#.decode("utf-8")
        self.save()
        return True

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return self.data.has_key(key)

    def __iter__(self):
        for key in self.data:
            yield key

    def __str__(self):
        return u"sid: %s, {%s}" % (self.sid, ', '.join(['"%s" = "%s"' % (k, self.data[k]) for k in self.data]))

def session(method):
    """Decorate methods with this to require that the user get session."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        sid = self.get_secure_cookie("session_id")
        session_instance = SessionManager()
        session_data = session_instance.get_session(sid)
        if (not sid)or(sid != session_data.sid):
            session_instance.save_session(session_data)
            self.set_secure_cookie("session_id", session_data.sid, 1)
        self.__setattr__("SESSION", session_data)
        return method(self, *args, **kwargs)
    return wrapper

def _unicode(s):
    if isinstance(s, str):
        try:
            return s.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPError(400, "Non-utf8 argument")
    assert isinstance(s, unicode)
    return s

def trans_64(s):
    try:
        s = int(s)
        return unicode(urlsafe_b64encode(str(s)))
    except ValueError:
        return int(urlsafe_b64decode(s))

