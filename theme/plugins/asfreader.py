"""
asfreader.py
----------------
Pelican plugin that processes Markdown files through as an ezt template then through GitHub Flavored Markdown.
"""

import os
from tempfile import NamedTemporaryFile

from pelican import signals
from pelican.utils import pelican_open

GFMReader = sys.modules['pelican-gfm.gfm'].GFMReader

class ASFReadertMixin:
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)

        # look for the ASFDATA yaml file
        print("ASFReaderMixin.__init__: %s" % self.settings("ASFDATA"))
        # read the ASFDATA yaml file
        # slurp the datasources
        # flatten for ezt

    def read(self, source_path):
        print("ASFReaderMixin.read: %s" % source_path)
        content, metadata = super().read(source_path)
        return content, metadata


class ASFReader(ASFReaderMixin, GFMReader):
    pass


def add_reader(readers):
    readers.reader_classes['emd'] = ASFReader


def register():
    signals.readers_init.connect(add_reader)
