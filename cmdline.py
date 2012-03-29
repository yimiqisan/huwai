#!/usr/bin/env python
# encoding: utf-8
"""
cmdline.py

Created by 刘 智勇 on 2011-11-08.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os

if __name__ == '__main__':
	cmd = 'from cmd import ' + sys.argv[1]
	exec(cmd)
	cmd = sys.argv[1] + '.run(sys.argv[2:])'
	exec(cmd)
