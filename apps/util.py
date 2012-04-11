#!/usr/bin/env python
# encoding: utf-8
"""
util.py

Created by 刘 智勇 on 2011-12-19.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import os, re, subprocess, sys, urllib
import logging
import atexit

from logging import DEBUG, INFO, WARN, ERROR, FATAL
from time import time
from collections import defaultdict
import tempfile as tf



logging.basicConfig(stream=sys.stderr, level=logging.INFO, 
                    format="%(levelname).1s %(filename)s:%(lineno)s -- %(message)s ")

def tempfile(conf):
  return tf.TemporaryFile(dir=conf['staging_directory'])
 
def execute(cmd):
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE).communicate()

def init_dir(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)
        
def remove_file(f):
  if os.path.exists(f):
    os.remove(f)


def currentFrame():
  return sys._getframe(6)

def findCaller():
  f = currentFrame()
  code = f.f_code
  return (code.co_filename, f.f_lineno, code.co_name)
      
logging.root.findCaller = findCaller

class Logger():
  @staticmethod
  def debug(fmt, *args, **kw):
    if logging.root.isEnabledFor(DEBUG): 
      logging.debug(fmt % args, **kw)
  
  @staticmethod  
  def info(fmt, *args, **kw):
    if logging.root.isEnabledFor(INFO): 
      logging.info(fmt % args, **kw)
  
  @staticmethod  
  def warn(fmt, *args, **kw): 
    if logging.root.isEnabledFor(WARN): 
      logging.warn(fmt % args, **kw)
      
  @staticmethod  
  def error(fmt, *args, **kw): 
    if logging.root.isEnabledFor(ERROR): 
      logging.error(fmt % args, **kw)
  
  @staticmethod  
  def fatal(fmt, *args, **kw): 
    if logging.root.isEnabledFor(FATAL): 
      logging.fatal(fmt % args, **kw)
  
log = Logger()

class TimeUtil():
  @staticmethod
  def time(f, *args):
    st = time()
    r = f(*args)
    ed = time()
    log.info('%s: result=%s, runtime=%4.2f', f.__name__, r, ed - st)
    return r
  
  def __init__(self):
    self.start()
  
  def start(self):
    self.start_time = time()    

  def reset(self, msg):
    if msg: self.finish(msg)
    self.start()
  
  def finish(self, msg):
    t = time() - self.start_time
    log.info('%s: runtime: %4.2f', msg, t)
    

class Stat():
  def __init__(self):
    self.time = 0
    self.count = 0
    self._t = []
  
  def start(self):
    self.count += 1
    self._t.append(time())
    
  def finish(self):
    v = self._t.pop()
    if not self._t:
      self.time += time() - v

    
  def __repr__(self):
    return '(%.2f %d)' % (self.time, self.count)

STATS = defaultdict(Stat)
    
class Flags():  
  def __init__(self):
    from argparse import ArgumentParser   
    self.parser = ArgumentParser()
    self.add_default_options()
    
  def parse(self, argv=None):
    if not argv:
      argv = sys.argv
    
    cmd = argv[0]
    options = self.parser.parse_args(argv[1:])
    
    for k in dir(options):
      if not k.startswith('_'):
        setattr(self, k, getattr(options, k))
        
    logging.getLogger().level = getattr(logging, self.log_level.upper())
    sys.argv = [cmd]
    
    if self.stats:  
      def dump_stats():
        for k, v in STATS.items():
          print >>sys.stderr, '%40s :: %s' % (k, v)
      atexit.register(dump_stats)
    
  def add_default_options(self):
    self.parser.add_argument("--profile", action="store_true", default=False, help="Capture profiling data.")
    self.parser.add_argument("--log_level", action="store", default="info")
    self.parser.add_argument("--stats", action="store_true", default=False, help="Dump statistics on pass timing.")
    
  def add_argument(self, *args, **kw):
    self.parser.add_argument(*args, **kw)
    
#flags = Flags()


class NamedList(object):
  '''List with values accessible by both key and by index.'''
  def __init__(self, keys, values):
    self.list = values
    self.keys = keys
    
    if len(keys) != len(values):
      raise ValueError, 'Mismatched lists to NamedList!'
    
    self.mapping = dict([(keys[i], i) for i in range(len(keys))]) 
    
  def __setitem__(self, k, v):     
    if not isinstance(k, int): 
      if not k in self.mapping:
        raise KeyError, 'New values cannot be added to NamedList.'
      k = self.mapping[k]
    
    if k >= len(self.list):
      raise KeyError, 'New values cannot be added to NamedList.'
    self.list[k] = v
  
  def __getitem__(self, k):
    if isinstance(k, int): return self.list[k]
    else: return self.list[self.mapping[k]]
    
  def __len__(self):
    return len(self.list)
  
  def __repr__(self):
    return '[' + ', '.join(['(%s, %s)' % (repr(self.keys[i]), repr(self.list[i])) for i in range(len(self.list)) ]) + ']'
  
  def __eq__(self, other):
    return self.list == other.list

  def __contains__(self, k):
    return k in self.keys

def shell(cmd):
  f = os.popen(cmd)
  r = f.read()
  f.close()
  return r

def hashable(v):
  try:
    hash(v)
    return True
  except:
    return False
  
def clean_string(v):
  if hasattr(v, '__name__'): v = v.__name__ 
  v = str(v)
  v = re.sub('[^a-zA-Z0-9_]', '', v)
  return v.lower()[:30]

def multi_get_letter(str_input):
    
    if isinstance(str_input, unicode):
        unicode_str = str_input
    else:
        try:
            unicode_str = str_input.decode('utf8')
        except:
            try:
                unicode_str = str_input.decode('gbk')
            except:
                print 'unknown coding'
                return
    
    return_list = []
    for one_unicode in unicode_str:
        print single_get_first(one_unicode)
        return_list.append(single_get_first(one_unicode))
    return "".join(return_list)    
    
def single_get_first(unicode1):
    str1 = unicode1.encode('gbk')
    try:        
        ord(str1)
        return str1
    except:
        asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536
        if asc >= -20319 and asc <= -20284:
            return 'a'
        if asc >= -20283 and asc <= -19776:
            return 'b'
        if asc >= -19775 and asc <= -19219:
            return 'c'
        if asc >= -19218 and asc <= -18711:
            return 'd'
        if asc >= -18710 and asc <= -18527:
            return 'e'
        if asc >= -18526 and asc <= -18240:
            return 'f'
        if asc >= -18239 and asc <= -17923:
            return 'g'
        if asc >= -17922 and asc <= -17418:
            return 'h'
        if asc >= -17417 and asc <= -16475:
            return 'j'
        if asc >= -16474 and asc <= -16213:
            return 'k'
        if asc >= -16212 and asc <= -15641:
            return 'l'
        if asc >= -15640 and asc <= -15166:
            return 'm'
        if asc >= -15165 and asc <= -14923:
            return 'n'
        if asc >= -14922 and asc <= -14915:
            return 'o'
        if asc >= -14914 and asc <= -14631:
            return 'p'
        if asc >= -14630 and asc <= -14150:
            return 'q'
        if asc >= -14149 and asc <= -14091:
            return 'r'
        if asc >= -14090 and asc <= -13119:
            return 's'
        if asc >= -13118 and asc <= -12839:
            return 't'
        if asc >= -12838 and asc <= -12557:
            return 'w'
        if asc >= -12556 and asc <= -11848:
            return 'x'
        if asc >= -11847 and asc <= -11056:
            return 'y'
        if asc >= -11055 and asc <= -10247:
            return 'z'
        return ''

def weather(provice, major):
    url="http://qq.ip138.com/weather/"+provice+'/'+major+'.htm'
    wetherhtml=urllib.urlopen(url)
    result=wetherhtml.read().decode('GB2312')#.encode('utf-8')
    #result=result.replace("gb2312","utf-8")
    f=file('weather.txt','w')
    f.write(result.encode('GB2312'))
    f.close()
    
    pattern='Title.+<b>(.+)</b>'
    Title=re.search(pattern,result).group(1)
    pattern='>(\d*-\d*-\d*.+?)<'
    date=re.findall(pattern,result)
    pattern='alt="(.+?)"'
    weather=re.findall(pattern,result)
    pattern='<td>([-]?\d{1,2}.+)</td>'
    temperature=re.findall(pattern,result)
    print "%35.30s"%Title,""
    length=len(date)
    for i in range(length):
        print '%30.20s'%date[i],'\t%s'%weather[i],'\t%s'%temperature[i]
