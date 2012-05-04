#! /usr/bin/env python
#coding=utf-8


from apps.note import Note

def run(argv):
    opts = {}
    n = Note()
    n._api.map(_handle_entity, opts)
    return
    
def _handle_entity(obj, opts):
    n = Note()
    n._api.edit(obj['_id'], channel=u'origin')
#    try:
#        tid = obj['added']['tid']
#    except:
#        tid = n._api._get_tid(obj['title'])
#    n._api.edit(obj['_id'], content=obj['content'][obj['added']['tid']])
    return True
