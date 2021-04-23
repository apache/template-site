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

'''
Find {#id} or {.class} trailing text
'''
ELEMENTID_RE = re.compile(r'(?:[ \t]*[{\[][ \t]*(?P<type>[#.])(?P<id>[-._:a-zA-Z0-9 ]+)[}\]])(\n|$)')

'''
Find heading tags
'''
HEADING_RE = re.compile(r'^h[1-6]')

IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')

LINK_CHAR = u'¶'

PARA_MAP = {
    ord('¶'): None
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
    if test_setting['debug']:
        for option in test_setting:
            print("Setting: %s: %s" % (option, test_setting[option]))

    title = content.metadata.get('title', 'Title')
    print("Testing %s" % content.path_no_ext)
    print(title)
    print(content._content)

    # content._content = soup.decode(formatter='html')


def register():
    signals.initialized.connect(init_default_config)


signals.page_generator_preread.connect(check_content)
