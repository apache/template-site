"""
asfreader.py
----------------
Pelican plugin that processes Markdown files through as an ezt template then through GitHub Flavored Markdown.
"""

import os
import sys

from tempfile import NamedTemporaryFile

from pelican import signals
from pelican.utils import pelican_open

GFMReader = sys.modules['pelican-gfm.gfm'].GFMReader

class ASFReader(GFMReader):
    def read(self, source_path):
        print("ASFReader,read: %s" % self.settings("ASF_DATA"))
        print("ASFReader.read: %s" % source_path)
        content, metadata = super().read(source_path)
        return content, metadata


def add_reader(readers):
    readers.reader_classes['emd'] = ASFReader


def register():
    signals.readers_init.connect(add_reader)
