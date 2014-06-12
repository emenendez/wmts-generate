wmts-generate
=============

Generate a WTMSCapabilities.xml file from a simple JSON config file

Dependencies
------------
- Jinja2
- MarkupSafe

Usage
-----
1. Create config.wmts with your service-specific values
2. `python wmts-generate.py config.wmts`