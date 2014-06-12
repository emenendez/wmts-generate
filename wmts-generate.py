from __future__ import print_function
import os
from jinja2 import Environment, FileSystemLoader
import config

# Global config
wmts = {
	'Version': '1.0.0',
	'ServiceMetadataFile': 'WMTSCapabilities.xml',
	'Template': 'wmts.xml',
}

# Add service-specifc config from config.py
wmts.update(config.wmts)

# Set up Jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(wmts['Template'])

# Create WMTS version folder
if not os.path.exists(wmts['Version']):
	os.mkdir(wmts['Version'])

# Write service metadata file
with open(wmts['Version'] + '/' + wmts['ServiceMetadataFile'], 'w') as output:
	output.write(template.render(wmts))
