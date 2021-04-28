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

TEST = {
    'debug': False
}

def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG

    DEFAULT_CONFIG.setdefault('TEST', TEST)
    if(pelican):
        pelican.settings.setdefault('TEST', TEST)


def check_content(content):
    if isinstance(content, contents.Static):
        return

    test_setting = content.settings['TEST']
    for option in test_setting:
        print("Setting: %s: %s" % (option, test_setting[option]))

    title = content.metadata.get('title', 'Title')
    print("Testing %s" % content.path_no_ext)
    print(title)
    print(content._content)


def register():
    signals.initialized.connect(init_default_config)


signals.content_object_init.connect(check_content)
