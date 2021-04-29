'''
asf_genid
===================================
Generates HeadingIDs, ElementID, and PermaLinks
First find all specified IDs and classes. Assure unique ID and permalonk
Next find all headings missing IDs. Assure unique ID and permalink
Generates a Table of Content
'''

from __future__ import unicode_literals

import logging
import re
import unicodedata
import sys

from bs4 import BeautifulSoup, Comment

from pelican import contents, signals


logger = logging.getLogger(__name__)

'''
https://github.com/waylan/Python-Markdown/blob/master/markdown/extensions/headerid.py
'''

ASF_GENID = {
    'metadata': True,
    'elements': True,
    'headings': True,
    'toc': True,
    'toc_headers': r"h[1-6]",
    'permalinks': True,
    'debug': False
}

'''
Find {#id} or {.class} trailing text
'''
ELEMENTID_RE = re.compile(r'(?:[ \t]*[{\[][ \t]*(?P<type>[#.])(?P<id>[-._:a-zA-Z0-9 ]+)[}\]])(\n|$)')

'''
Find {{ metadata }}
'''
METADATA_RE = re.compile(r'{{\s*(?P<meta>[-._:a-zA-Z0-9]+)\s*}}')

'''
Find heading tags
'''
HEADING_RE = re.compile(r'^h[1-6]')

IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')

LINK_CHAR = u'¶'

PARA_MAP = {
    ord('¶'): None
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

    DEFAULT_CONFIG.setdefault('ASF_GENID', ASF_GENID)
    if(pelican):
        pelican.settings.setdefault('ASF_GENID', ASF_GENID)


def slugify(value, separator):
    """ Slugify a string, to make it URL friendly. """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub('[^\w\s-]', '', value.decode('ascii')).strip().lower()
    return re.sub('[%s\s]+' % separator, separator, value)


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
    new_tag = soup.new_tag('a', href="#" + mod_element['id'])
    new_tag['class'] = "headerlink"
    new_tag['title'] = "Permalink"
    new_tag.string = LINK_CHAR
    mod_element.append(new_tag)


def generate_id(content):
    if isinstance(content, contents.Static):
        return

    asf_genid = content.settings['ASF_GENID']
    # if asf_genid['debug']:
    #    for option in asf_genid:
    #        print("Setting: %s: %s" % (option, asf_genid[option]))

    #    for name in content.settings['PLUGINS']:
    #        print("Plugin: %s" % name)

    #    for module in sys.modules:
    #        print("Module: %s" % module)

    ids = set()
    soup = BeautifulSoup(content._content, 'html.parser')
    title = content.metadata.get('title', 'Title')
    content.metadata['relative_source_path'] = content.relative_source_path

    if asf_genid['debug']:
        print("Metadata inclusion in %s" % content.relative_source_path)
    if asf_genid['metadata']:
        for tag in soup.findAll(string=METADATA_RE):
            this_string = str(tag.string)
            m = 1
            modified = False
            while m:
                m = METADATA_RE.search(this_string)
                if m:
                    print(this_string)
                    this_string = re.sub(METADATA_RE,
                                         content.metadata.get(m.group(1),''),
                                         this_string)
                    modified = True
            if modified:
                print(this_string)
                tag.string.replace_with(this_string)

    if asf_genid['debug']:
        print("Directory of ids already in %s" % content.relative_source_path)
    # Find all id attributes already present
    for tag in soup.findAll(id=True):
        unique(tag["id"], ids)
        # don't change existing ids

    if asf_genid['elements']:
        if asf_genid['debug']:
            print("Checking for elementid in %s" % content.relative_source_path)
        # Find all {#id} and {.class} text and assign attributes
        for tag in soup.findAll(string=ELEMENTID_RE):
            tagnav = tag.parent
            this_string = str(tag.string)
            if asf_genid['debug']:
                print("name = %s, string = %s" % (tagnav.name, this_string))
            if tagnav.name not in ['[document]', 'code', 'pre']:
                m = ELEMENTID_RE.search(tag.string)
                if m:
                    tag.string.replace_with(this_string[:m.start()])
                    if m.group('type') == '#':
                        tagnav['id'] = unique(m.group('id'), ids)
                        if asf_genid['permalinks']:
                            permalink(soup, tagnav)
                            if asf_genid['debug']:
                                print(tagnav)
                    else:
                        tagnav['class'] = m.group('id')
                        if asf_genid['debug']:
                            print("Class %s : %s" % (tag.name, tagnav['class']))

    if asf_genid['headings']:
        if asf_genid['debug']:
            print("Checking for headings in %s" % content.relative_source_path)
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
            new_id = slugify(new_string,'-')
            tag['id'] = unique(new_id, ids)
            if asf_genid['permalinks']:
                permalink(soup, tag)
                if asf_genid['debug']:
                    print(tag)

    if asf_genid['toc']:
        # Find TOC tag
        tocTag = soup.find('p', text='[TOC]')
        if tocTag:
            # Generate ToC from headings following the [TOC]
            settoc = False
            tree = node = HtmlTreeNode(None, title, 'h0', '')
            heading_re = re.compile(asf_genid['toc_headers'])
            for header in tocTag.findAllNext(heading_re):
                settoc = True
                node, new_header = node.add(header)

            if settoc:
                if asf_genid['debug']:
                    print("Generating ToC for %s" % content.relative_source_path)
                # convert the HtmlTreeNode into Beautiful soup
                tree_string = '{}'.format(tree)
                tree_soup = BeautifulSoup(tree_string, 'html.parser')
                content.toc = tree_soup.decode(formatter='html')
                if asf_genid['debug']:
                    print(content.toc)
                tocTag.replaceWith(tree_soup)

    if asf_genid['debug']:
        print("Reflowing content in %s" % content.relative_source_path)
    content._content = soup.decode(formatter='html')


def register():
    signals.initialized.connect(init_default_config)


signals.content_object_init.connect(generate_id)
