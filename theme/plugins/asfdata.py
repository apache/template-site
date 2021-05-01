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

from pelican import signals

import pelican.utils
import os.path
import requests
import yaml
import json

ASF_DATA = {
    'metadata': { },
    'debug': False
}


def read_config(config_yaml):
    with pelican.utils.pelican_open(config_yaml) as text:
        config_data = yaml.load(text)
        print(config_data)
    return config_data


def url_data(url):
    content = requests.get(url).text
    parts = url.split('/')
    extension = os.path.splitext(parts[-1])[1]  # split off ext, keep ext
    if extension == ".json":
        load = json.loads(content)
    elif extension == ".yaml":
        load = yaml.load(content)
    else:
        load = { }
    return load


def load_splits(metadata, value, key, load):
    if 'splits' in value:
        for split in value['splits']:
            ref = value['splits'][split][0]
            print(f"{split} {ref}")
            reference = load[ref]
            metadata[split] = reference
    else:
        # no splits the whole loaded content is the saved dict
        metadata[key] = load


def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG

    print("-----\nasfdata")
    DEFAULT_CONFIG.setdefault('ASF_DATA', ASF_DATA)
    if pelican:
        pelican.settings.setdefault('ASF_DATA', ASF_DATA)

        asf_data = pelican.settings.get('ASF_DATA', DEFAULT_CONFIG['ASF_DATA'])
        for key in asf_data:
            print(f"config: [{key}] = {asf_data[key]}")
        
        if 'metadata' in asf_data:
            metadata = asf_data['metadata']
        else:
            metadata = { }
        if 'data' in asf_data:
            print(f"Processing {asf_data['data']}")
            config_data = read_config(asf_data['data'])
            for key in config_data:
                value = config_data[key]
                if isinstance(value, dict):
                    print(f"{key} is a dict")
                    print(value)
                    if 'url' in value:
                        load = url_data(value['url'])
                        load_splits(metadata, value, key, load)
                    else:
                        metadata[key] = value
                else:
                    print(f"{key} = {value}")
                    metadata[key] = value
        for key in metadata:
            print(f"metadata[{key}]")
        pelican.settings['ASF_DATA']['metadata'] = metadata
        print("-----")

def register():
    signals.initialized.connect(init_default_config)
