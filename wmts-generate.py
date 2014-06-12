from __future__ import print_function
from jinja2 import Environment, FileSystemLoader
from config import wmts

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('wmts.xml')
print(template.render(wmts))