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
# asfdata.py -- Pelican plugin that processes a yaml specification of data into a setting directory
#

from __future__ import unicode_literals

from pelican import utils, signals

import yaml

ASF_DATA = {
    'metadata': { },
    'debug': False
}

TEST_DATA = {
    'tester': 'Test Data'
}


def read_config(config_yaml):
    with pelican.utils.pelican_open(config_yaml) as text:
        config_data = yaml.load(text)
        print(config_data)
    return config_data


def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG

    DEFAULT_CONFIG.setdefault('ASF_DATA', ASF_DATA)
    if pelican:
        pelican.settings.setdefault('ASF_DATA', ASF_DATA)

        asf_data = pelican.settings.get('ASF_DATA', DEFAULT_CONFIG['ASF_DATA'])
        for key in asf_data:
            print(f"asfdata: [{key}] = {asf_data[key]}")
        key = 'data'
        if key in asf_data:
            print(f"Processing {asf_data[key]}")
            config_data = read_config(asf_data[key])
            pelican.settings['ASF_DATA']['metadata'] = TEST_DATA

def register():
    signals.initialized.connect(init_default_config)
