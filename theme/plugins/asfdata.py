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
    if pelican:
        pelican.settings.setdefault('ASFDATA', ASFDATA)

        asfdata = pelican.settings('ASFDATA')
        for key in asfdata:
            print("ASFDATA[%s] = %s" % (key,asfdata[key]))


def register():
    signals.initialized.connect(init_default_config)
