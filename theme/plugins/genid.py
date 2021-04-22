'''
genid
===================================
Generates HeadingIDs, ElementID, and PermaLinks
First find all specified IDs and classes. Assure unique ID and permalonk
Next find all headings missing IDs. Assure unique ID and permalink
Generates a Table of Content
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

GENID = {
    'elements' : True,
    'headings' : True,
    'toc' : True,
    'toc_headers' : r"h[1-6]",
    'permalinks' : True,
    'debug' : False
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

# An item in a Table of Contents
class HtmlTreeNode(object):
    def __init__(self, parent, header, level, id):
        self.children = []
        self.parent = parent
        self.header = header
        self.level = level
        self.id = id

    def add(self, new_header):
        new_level = new_header.name
        new_string = new_header.string
        new_id = new_header.attrs.get('id')

        if not new_string:
            new_string = new_header.find_all(
                text=lambda t: not isinstance(t, Comment),
                recursive=True)
            new_string = "".join(new_string)
        new_string = new_string.translate(PARA_MAP)

        if(self.level < new_level):
            new_node = HtmlTreeNode(self, new_string, new_level, new_id)
            self.children += [new_node]
            return new_node, new_header
        elif(self.level == new_level):
            new_node = HtmlTreeNode(self.parent, new_string, new_level, new_id)
            self.parent.children += [new_node]
            return new_node, new_header
        elif(self.level > new_level):
            return self.parent.add(new_header)

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

    DEFAULT_CONFIG.setdefault('GENID', GENID)
    if(pelican):
        pelican.settings.setdefault('GENID', GENID)


def unique(id, ids):
    """ Ensure id is unique in set of ids. Append '_1', '_2'... if not """
    while id in ids or not id:
        m = IDCOUNT_RE.match(id)
        print("id=\"%s\" is a duplicate" & id)
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

def generate_id(content):
    if isinstance(content, contents.Static):
        return

    genid = content.settings['GENID']
    if genid['debug']:
        for option in genid:
            print("Setting: %s: %s" % (option,genid[option]))

        for name in content.settings['PLUGINS']:
            print("Plugin: %s" % name)

        
    ids = set()
    soup = BeautifulSoup(content._content, 'html.parser')
    title = content.metadata.get('title', 'Title')

    if genid['debug']:
        print("Directory of ids already in %s" % content.path_no_ext)
    # Find all id attributes already present
    for tag in soup.findAll(id=True):
        this_id = unique(tag["id"], ids)
        # don't change existing ids

    if genid['elements']:
        if genid['debug']:
            print("Checking for elementid in %s" % content.path_no_ext)
        # Find all {#id} and {.class} text and assign attributes
        for tag in soup.findAll(string=ELEMENTID_RE):
            tagnav = tag.parent
            this_string = str(tag.string)
            if genid['debug']:
                print("name = %s, string = %s" % (tagnav.name, this_string))
            if tagnav.name not in ['[document]', 'code', 'pre']:
                m = ELEMENTID_RE.search(tag.string)
                if m:
                    tag.string.replace_with(this_string[:m.start()])
                    if m.group('type') == '#':
                        tagnav['id'] = unique(m.group('id'), ids)
                        if genid['permalinks']:
                            permalink(soup, tagnav)
                            if genid['debug']:
                                print(tagnav)
                    else:
                        tagnav['class'] = m.group('id')
                        if genid['debug']:
                            print("Class %s : %s" % (tag.name,tagnav['class']))

    if genid['headings']:
        if genid['debug']:
            print("Checking for headings in %s" % content.path_no_ext)
        # Find all headings w/o ids already present or assigned with {#id} text
        for tag in soup.findAll(HEADING_RE, id=False):
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
            if genid['debug']:
                print("Slug %s : %s : %s" % (tag['id'],new_slug,new_string))
            if genid['permalinks']:
                permalink(soup, tag)
                if genid['debug']:
                    print(tag)

    if genid['toc']:
        # Find TOC tag
        tocTag = soup.find('p', text='[TOC]')
        if tocTag:
            # Generate ToC from headings following the [TOC]
            settoc = False
            tree = node = HtmlTreeNode(None, title, 'h0', '')
            heading_re = re.compile(genid['toc_headers'])
            for header in tocTag.findAllNext(heading_re):
                settoc = True
                node, new_header = node.add(header)

            if settoc:
                if genid['debug']:
                    print("Generating ToC for %s" % content.path_no_ext)
                # convert the HtmlTreeNode into Beautiful soup
                tree_string = '{}'.format(tree)
                tree_soup = BeautifulSoup(tree_string, 'html.parser')
                content.toc = tree_soup.decode(formatter='html')
                if genid['debug']:
                    print(content.toc)
                tocTag.replaceWith(tree_soup)

    if genid['debug']:
        print("Reflowing content in %s" % content.path_no_ext)
    content._content = soup.decode(formatter='html')


def register():
    signals.initialized.connect(init_default_config)


signals.content_object_init.connect(generate_id)
