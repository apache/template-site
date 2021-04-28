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

ASFDATA = {
    'ignore': True,
    'debug': False
}

def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG

    DEFAULT_CONFIG.setdefault('ASFDATA', ASFDATA)
    print("default is set")
    if pelican:
        pelican.settings.setdefault('ASFDATA', ASFDATA)
        print("pelican.settings default is set")

        asf_data = pelican.settings.get('ASFDATA', DEFAULT_CONFIG['ASFDATA'])
        print(asf_data)
        for key in asf_data:
            print("ASFDATA[%s] = %s" % (key,asf_data[key]))


def register():
    signals.initialized.connect(init_default_config)
