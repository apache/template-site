#!/usr/bin/python -B
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#
# asfcheck.py -- Pelican plugin that checks page count.
#

import os.path
import sys
import random
import json
import traceback
import operator
import pprint

import requests
import yaml
import ezt

import xml.dom.minidom

import pelican.plugins.signals
import pelican.utils
from pelican.generators import (PagesGenerator)


ASF_CHECK = {
    'pages': 0,
    'debug': False,
}


# create metadata according to instructions.
def check_page_data(pel_ob):
    print('-----\nasfcheck')

    asf_check = pel_ob.settings.get('ASF_CHECK')

    if not asf_check:
        print('This Pelican installation is not using ASF_CHECK')
        return

    for key in asf_check:
        print(f'config: [{key}] = {asf_check[key]}')

    debug = asf_check['debug']
    min_pages = asf_check['pages']
    generators = pel_ob._get_generator_classes()
    pages_generator = next(g for g in generators
                           if isinstance(g, PagesGenerator))
    actual_pages = len(pages_generator.pages)
    print(f'-----\nminimum: {min_pages}; actual: {actual_pages}')


def tb_finalized(pel_ob):
    """ Print any exception, before Pelican chews it into nothingness."""
    try:
        check_page_data(pel_ob)
    except:
        print('-----', file=sys.stderr)
        traceback.print_exc()
        raise


def register():
    # Hook the "initialized" signal, to load our custom data.
    pelican.plugins.signals.finalized.connect(tb_finalized)
