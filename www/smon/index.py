#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import html
import os
import sys
sys.path.append(os.path.join(sys.path[0], os.path.dirname('/opt/smon/')))
import sql
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('template/'))
template = env.get_template('index.html')

print("Content-type: text/html\n\n")
template = template.render(services=sql.list())											
print(template)