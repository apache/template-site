'''
test
===================================
See what's what with signals and data
'''

from __future__ import unicode_literals

import logging
import re

from pelican import contents, signals


logger = logging.getLogger(__name__)

'''
https://github.com/waylan/Python-Markdown/blob/master/markdown/extensions/headerid.py
'''

ASF_DATA = {
    'process': False,
    'debug': False
}

def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG

    DEFAULT_CONFIG.setdefault('ASF_DATA', ASF_DATA)
    if pelican:
        pelican.settings.setdefault('ASF_DATA', ASF_DATA)

        asf_data = pelican.settings.get('ASF_DATA', DEFAULT_CONFIG['ASF_DATA'])
        print(asf_data)
        for key in asf_data:
            print("ASF_DATA[%s] = %s" % (key,asf_data[key]))
        if asf_data['process']:
            print("Processing %s" % asf_data['data'])

def register():
    signals.initialized.connect(init_default_config)
