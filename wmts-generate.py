from __future__ import print_function
import argparse
import json
import os
import re
from jinja2 import Environment, FileSystemLoader

# Global config
wmts = {
	'Version': '1.0.0',
	'ServiceMetadataFile': 'WMTSCapabilities.xml',
	'Template': 'wmts.xml',
}


# From https://github.com/getify/JSON.minify/blob/master/minify_json.py:
'''
Created on 20/01/2011

v0.2 (C) Gerald Storer
MIT License

Based on JSON.minify.js:
https://github.com/getify/JSON.minify

Contributers:
 - Pradyun S. Gedam (conditions and variable names changed)
'''

def json_minify(string, strip_space=True):
    tokenizer = re.compile('"|(/\*)|(\*/)|(//)|\n|\r')
    end_slashes_re = re.compile(r'(\\)*$')

    in_string = False
    in_multi = False
    in_single = False

    new_str = []
    index = 0

    for match in re.finditer(tokenizer, string):

        if not (in_multi or in_single):
            tmp = string[index:match.start()]
            if not in_string and strip_space:
                # replace white space as defined in standard
                tmp = re.sub('[ \t\n\r]+', '', tmp)
            new_str.append(tmp)

        index = match.end()
        val = match.group()

        if val == '"' and not (in_multi or in_single):
            escaped = end_slashes_re.search(string, 0, match.start())

            # start of string or unescaped quote character to end string
            if not in_string or (escaped is None or len(escaped.group()) % 2 == 0):
                in_string = not in_string
            index -= 1 # include " character in next catch
        elif not (in_string or in_multi or in_single):
            if val == '/*':
                in_multi = True
            elif val == '//':
                in_single = True
        elif val == '*/' and in_multi and not (in_string or in_single):
            in_multi = False
        elif val in '\r\n' and not (in_multi or in_string) and in_single:
            in_single = False
        elif not ((in_multi or in_single) or (val in ' \r\n\t' and strip_space)):
            new_str.append(val)

    new_str.append(string[index:])
    return ''.join(new_str)
# End https://github.com/getify/JSON.minify/blob/master/minify_json.py

# Command-line arguments
parser = argparse.ArgumentParser(description='Generate a WMTS Capabilities XML file.')
parser.add_argument('config', nargs='?', type=argparse.FileType('r'), default='default.wmts', help='WMTS service configuration file (default: default.wmts)')
args = parser.parse_args()

# Load config
config = json_minify(args.config.read())  # Read in config file and strip comments
args.config.close()
wmts.update(json.loads(config))  # Add service-specifc config to global config

# Set up Jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(wmts['Template'])

# Create WMTS version folder
if not os.path.exists(wmts['Version']):
	os.mkdir(wmts['Version'])

# Write service metadata file
with open(wmts['Version'] + '/' + wmts['ServiceMetadataFile'], 'w') as output:
	output.write(template.render(wmts))
