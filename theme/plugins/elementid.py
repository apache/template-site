'''
elementid
===================================
Generates HeadingIDs, ElementID, and PermaLinks
First find all specified IDs and classes. Assure unique ID and permalonk
Next find all headings missing IDs. Assure unique ID and permalink
'''

from __future__ import unicode_literals

import logging
import re

from bs4 import BeautifulSoup, Comment

from pelican import contents, signals
from pelican.utils import slugify


logger = logging.getLogger(__name__)

'''
https://github.com/waylan/Python-Markdown/blob/master/markdown/extensions/headerid.py
'''

'''
Find {#id} or {.class} trailing text
'''
ELEMENTID_RE = re.compile(r"""[ \t]*   # optional whitespace
                       [#]{0,6} # end of heading
                       [ \t]*   # optional whitespace
                       (?:[ \t]*[{\[][ \t]*(?P<type>[#.])(?P<id>[-._:a-zA-Z0-9 ]+)[}\]])
                       [ \t]*   # optional whitespace
                       (\n|$)   #  ^^ group('id') = id attribute
                    """,
                    re.VERBOSE)

'''
Find heading tags
'''
HEADING_RE = re.compile(r'^h[1-6]')

IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')

LINK_CHAR = u'¶'

CHARACTER_MAP = {
    ord('\n') : '-',
    ord('\t') : '-',
    ord('\r') : None,
    ord(' ') : '-',
    ord('\'') : None,
    ord('\"') : None,
    ord('?') : None,
    ord('/') : None,
     ord(',') : None,
    ord('.') : None,
    ord('(') : None,
    ord(')') : None,
    8216 : None,
    8217 : None,
    8218 : None,
    8219 : None,
    8220 : None,
    8221 : None,
    8222 : None,
    8223 : None,
    ord('¶') : None
}

def unique(id, ids):
    """ Ensure id is unique in set of ids. Append '_1', '_2'... if not """
    while id in ids or not id:
        m = IDCOUNT_RE.match(id)
        if m:
            id = '%s_%d' % (m.group(1), int(m.group(2)) + 1)
        else:
            id = '%s_%d' % (id, 1)
    ids.add(id)
    return id

def mod(mod_element, ids):

def permalink(soup, mod_element):
    new_tag = soup.new_tag('a', href="#"+mod_element['id'])
    new_tag['class'] = "headerlink"
    new_tag['title'] = "Permalink"
    new_tag.string = LINK_CHAR
    mod_element.append(new_tag)
    print("Perm %s : %s" % (mod_element.name,new_tag['href']))

def generate_elementid(content):
    if isinstance(content, contents.Static):
        return

    all_ids = set()
    soup = BeautifulSoup(content._content, 'html.parser')

    # Find all {#id} and {.class} attr tags
    for tag in soup.findAll(string=ELEMENTID_RE):
        if tag.name not in ['code', 'pre']:
            m = ELEMENTID_RE(tag.string)
            if m.group('type') == '#':
                new_id = m.group('id')
                tag.string = tag.string[:m.start()]
                tag['id'] = unique(new_id, ids)
                permalink(soup, tag)
            else:
                tag['class'] = m.group('id')
                tag.string = tag.string[:m.start()]
                print("Class %s : %s" % (tag.name,tag['class']))

    # Find all headings
    for tag in soup.findAll(HEADING_RE):
        if not tag['id']:
            new_string = tag.string
            if not new_string:
                # roll up strings if no immediate string
                new_string = tag.find_all(
                    text=lambda t: not isinstance(t, Comment),
                    recursive=True)
                new_string = "".join(new_string)

            new_id = tag['id']
            if not new_id:
                # don't have an id then createit from text
                new_slug = new_string.translate(CHARACTER_MAP)
                new_id = slugify(new_slug)
                tag['id'] = unique(new_id, ids)
                print("Slug %s : %s : %s" % (tag.['id'],new_slug,new_string))
                permalink(soup, tag)
            else:
                # existing ids are assumed to be covered by {#id} form
                ids.add(new_id)

    content._content = soup.decode(formatter='html')


def register():
    signals.initialized.connect(init_default_config)


signals.content_object_init.connect(generate_elementid)
