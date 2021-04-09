#!/usr/bin/env python
# -*- coding: utf-8 -*- #
# vim: encoding=utf-8
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import unicode_literals
from datetime import date

# import os
# import sys


PATH = 'content'

TIMEZONE = 'UTC'

DEFAULT_LANG = u'en'
AUTHOR = u'Template Community'
SITENAME = u'Apache Template'
SITEDOMAIN = 'template.apache.org'
SITEURL = 'https://template.apache.org'
SITELOGO = 'https://template.apache.org/images/logo.png'
SITEDESC = u'Assists external project communities interested in becoming an Apache project learn how The ASF works and its views on how to build a healthy community'
TRADEMARKS = u'Apache, the Apache feather logo, and Template are trademarks or registered trademarks'
SITEREPOSITORY = 'https://github.com/apache/template-site/blob/master/content/pages/'
CURRENTYEAR = date.today().year

# Save pages using full directory preservation
PAGES_PATHS = ['content']
# PATH_METADATA= '(?P<path_no_ext>.*)\..*'
# PAGE_SAVE_AS= '{path_no_ext}.html'
PAGE_URL = '{slug}.html'
SLUGIFY_SOURCE = 'basename'
PAGE_SAVE_AS = '{slug}.html'

# We want to serve info.yaml and template.rdf in addition to any images
STATIC_PATHS = ['.htaccess', 'info.yaml', 'template.rdf', 'images']

# We don't use articles, but we don't want pelican to think
# that content/ contains articles.
ARTICLE_PATHS = ['articles']

# Disable these pages
ARCHIVES_SAVE_AS = ''
ARTICLE_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
INDEX_SAVE_AS = ''
TAGS_SAVE_AS = ''

# Enable ATOM feed and Disable other feeds
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Pelican Plugins
# The provided location. If the buildbot does not have a new plugin then look into requirements.txt
PLUGIN_PATHS = ['./theme/plugins']
PLUGINS = ['toc', 'pelican-gfm', 'sitemap']

# Markdown Configuration
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.extra': {},
        'markdown.extensions.admonition': {},
        'markdown.extensions.codehilite': {
            'css_class': 'highlight'
        },
        'smarty' : {
            'smart_angled_quotes' : 'true'
        },
        'markdown.extensions.toc': {
            'permalink': 'true',
        },
    }
}

# TOC Generator
TOC_HEADERS = r"h[1-6]"

# Sitemap Generator
SITEMAP = {
    "exclude": ["tag/", "category/"],
    "format": "xml",
    "priorities": {
        "articles": 0.1,
        "indexes": 0.1,
        "pages": 0.8
    },
    "changefreqs": {
        "articles": "never",
        "indexes": "never",
        "pages": "monthly"
    }
}

# Unused links
LINKS = ( )
SOCIAL = ( )

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
