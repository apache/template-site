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
# asfreader.py -- Pelican plugin that processes ezt template Markdown through ezt and  then GitHub Flavored Markdown.
#

import sys
import io
import os
import traceback

import re
import ezt

import pelican.plugins.signals
import pelican.readers
import pelican.settings


# create metadata according to instructions.
def config_copy_data(pel_ob):
    print('-----\nasfcopy')

    output_path = pel_ob.settings.get('OUTPUT_PATH')
    path = pel_ob.settings.get('PATH')
    print(f'{path} --> {output_path}')
    asf_copy = pel_ob.settings.get('ASF_COPY')
    if asf_copy:
        print(asf_copy)
    else:
        print("Nothing to copy")


def tb_finalized(pel_ob):
    """ Print any exception, before Pelican chews it into nothingness."""
    try:
        config_copy_data(pel_ob)
    except Exception:
        print('-----', file=sys.stderr)
        traceback.print_exc()
        # exceptions here stop the build
        raise


def register():
    pelican.plugins.signals.finalized.connect(tb_finalized)
