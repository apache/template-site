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

import pelican.plugins.signals
import pelican.utils
import os.path
import requests
import random
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


def remove_part(reference, part):
    for refs in reference:
        if refs == part:
            del reference[part]
            return
        elif isinstance(reference[refs], dict):
            remove_part(reference[refs], part)


def where_parts(reference, part):
    # currently only works on True parts
    filtered = [ ]
    for refs in reference:
        if not reference[refs][part]:
            filtered.append(refs)
    for refs in filtered:
        del reference[refs]


def alpha_part(reference, part):
    for refs in reference:
        name = reference[refs][part]
        if name == 'HTTP Server':
            # when sorting by letter HTTPD Server is wanted first
            letter = ' '
        else:
            letter = name[0]
        print(f"{letter} {name}")
        reference[refs]['letter'] = letter


def asfid_part(reference, part):
    print(f"asfid {part}")
    for refs in reference:
        fix = reference[refs][part]
        for k in fix:
            availid = k
            name = fix[k]['name']
        print(f"{name} ({availid})")
        reference[refs][part] = name
        reference[refs]['availid'] = availid


def sequence_dict(reference):
    sequence = [ ]
    for refs in reference:
        if isinstance(reference[refs],dict):
            reference[refs]['key_id'] = refs
            sequence.append(reference[refs])
    return sequence


def process_sequence(metadata, seq, sequence, load):
    reference = load
    is_sequence = False

    # description
    if 'description' in sequence:
        print(f"{seq} is {sequence['description']}")

    # select sub dictionary
    if 'path' in sequence:
        parts = sequence['path'].split('.')
        for part in parts:
            reference = reference[part]

    # filter dictionary by attribute value. if filter is false discard
    if 'where' in sequence:
        where_parts(reference, sequence['where'])

    # remove irrelevant keys
    if 'trim' in sequence:
        parts = sequence['trim'].split(',')
        for part in parts:
            remove_part(reference, part)

    # transform roster and chair patterns
    if 'asfid' in sequence:
        asfid_part(reference, sequence['asfid'])

    # add first letter ofr alphabetic categories
    if 'alpha' in sequence:
        alpha_part(reference, sequence['alpha'])

    # this sequence is derived from another sequence
    if 'sequence' in sequence:
        reference = metadata[sequence['sequence']]
        is_sequence = True

    # this sequence is a random sample of another sequence
    if 'random' in sequence:
        if is_sequence:
            reference = random.sample(reference, sequence['random'])
        else:
            print(f"{seq} - first specify the sequence to sample")

    # convert the dictionary to a sequence
    if not is_sequence:
        reference = sequence_dict(reference)

    # save sequence in metadata
    metadata[seq] = reference


def process_load(metadata, value, key, load):
    for seq in value:
        if seq != 'url':
            # sequence
            sequence = value[seq]
            process_sequence(metadata, seq, sequence, load)


def config_read_data(pelican):
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
                        process_load(metadata, value, key, load)
                    else:
                        metadata[key] = value
                else:
                    print(f"{key} = {value}")
                    metadata[key] = value

        pelican.settings['ASF_DATA']['metadata'] = metadata
        print("-----")
        for key in metadata:
            print(f"metadata[{key}] =")
            print(metadata[key])
            print("-----")

def register():
    pelican.plugins.signals.initialized.connect(config_read_data)
