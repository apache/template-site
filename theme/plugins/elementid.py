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

PARA_MAP = {
    ord('¶') : None
}

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

class HtmlTreeNode(object):
    def __init__(self, parent, header, level, id):
        self.children = []
        self.parent = parent
        self.header = header
        self.level = level
        self.id = id

    def add(self, new_header, ids):
        new_level = new_header.name
        new_string = new_header.string
        new_id = new_header.attrs.get('id')

        if not new_string:
            new_string = new_header.find_all(
                text=lambda t: not isinstance(t, Comment),
                recursive=True)
            new_string = "".join(new_string)
        new_string = new_string.translate(PARA_MAP)

        new_header.attrs['id'] = new_id
        if(self.level < new_level):
            new_node = HtmlTreeNode(self, new_string, new_level, new_id)
            self.children += [new_node]
            return new_node, new_header
        elif(self.level == new_level):
            new_node = HtmlTreeNode(self.parent, new_string, new_level, new_id)
            self.parent.children += [new_node]
            return new_node, new_header
        elif(self.level > new_level):
            return self.parent.add(new_header, ids)

    def __str__(self):
        ret = ""
        if self.parent:
            ret = "<a class='toc-href' href='#{0}' title='{1}'>{1}</a>".format(
                self.id, self.header)

        if self.children:
            ret += "<ul>{}</ul>".format('{}' * len(self.children)).format(
                *self.children)

        if self.parent:
            ret = "<li>{}</li>".format(ret)

        if not self.parent:
            ret = "<div id='toc'>{}</div>".format(ret)

        return ret


def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG

    TOC_DEFAULT = {
        'TOC_HEADERS': '^h[1-6]',
        'TOC_RUN': 'true'
    }

    DEFAULT_CONFIG.setdefault('TOC', TOC_DEFAULT)
    if(pelican):
        pelican.settings.setdefault('TOC', TOC_DEFAULT)


def generate_toc(soup, content, title, ids):

    settoc = False
    tree = node = HtmlTreeNode(None, title, 'h0', '')

    # Find TOC tag
    tocTag = soup.find('p', text='[TOC]')
    if tocTag:
        for header in tocTag.findAllNext(HEADING_RE):
            settoc = True
            node, new_header = node.add(header, ids)
            header.replaceWith(new_header)  # to get our ids back into soup

        if settoc:
            print("Generating ToC for %s" % content.path_no_ext)
            tree_string = '{}'.format(tree)
            tree_soup = BeautifulSoup(tree_string, 'html.parser')
            content.toc = tree_soup.decode(formatter='html')
            itoc = soup.find('p', text='[TOC]')
            if itoc:
                itoc.replaceWith(tree_soup)

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

    try:
        header_re = re.compile(content.metadata.get(
            'toc_headers', content.settings['TOC']['TOC_HEADERS']))
    except re.error as e:
        logger.error("TOC_HEADERS '%s' is not a valid re\n%s",
                     content.settings['TOC']['TOC_HEADERS'])
        raise e

    for name in content.settings['PLUGINS']:
        print("Plugin: %s" % name)

    ids = set()
    soup = BeautifulSoup(content._content, 'html.parser')

    print("Checking for elementid in %s" % content.path_no_ext)
    # Find all {#id} and {.class} attr tags
    for tag in soup.findAll(string=ELEMENTID_RE):
        if tag.name not in ['code', 'pre']:
            this_string = str(tag.string)
            print(this_string)
            m = ELEMENTID_RE.match(this_string)
            if m.group('type') == '#':
                new_id = m.group('id')
                print("id = %s" % new_id)
                tag.string.replace_with(this_string[:m.start()])
                tag['id'] = unique(new_id, ids)
                permalink(soup, tag)
            else:
                tag['class'] = m.group('id')
                print("class = %s" % tag['class'])
                tag.string.replace_with(this_string[:m.start()])
                print("Class %s : %s" % (tag.name,tag['class']))

    print("Checking for headings in %s" % content.path_no_ext)
    # Find all headings
    for tag in soup.findAll(HEADING_RE, id=False):
        print("heading %s" % tag.name)
        new_string = tag.string
        if not new_string:
            # roll up strings if no immediate string
            new_string = tag.find_all(
                text=lambda t: not isinstance(t, Comment),
                recursive=True)
            new_string = "".join(new_string)

        # don't have an id then createit from text
        new_slug = new_string.translate(CHARACTER_MAP)
        new_id = slugify(new_slug)
        tag['id'] = unique(new_id, ids)
        print("Slug %s : %s : %s" % (tag['id'],new_slug,new_string))
        permalink(soup, tag)

    print("Reflowing content in %s" % content.path_no_ext)

    title = content.metadata.get('title', 'Title')
    generate_toc(soup, content, title, ids)
    content._content = soup.decode(formatter='html')


def register():
    signals.initialized.connect(init_default_config)


signals.content_object_init.connect(generate_elementid)
