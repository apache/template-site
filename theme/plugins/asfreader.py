"""
asfreader.py
----------------
Pelican plugin that processes Markdown files through as an ezt template then through GitHub Flavored Markdown.
"""

import os
import sys
import io
import ezt

from tempfile import NamedTemporaryFile

from pelican import signals
from pelican.utils import pelican_open

GFMReader = sys.modules['pelican-gfm.gfm'].GFMReader

class ASFReader(GFMReader):
    def read(self, source_path):
        print("ASFReader.read: %s" % source_path)
        content, metadata = super().read(source_path)
        template = None
        with NamedTemporaryFile(delete=False) as f:
            f.write(content.encode('utf-8'))
            f.close()
            # template = ezt.Template(f.name, compress_whitespace=0, base_format=ezt.FORMAT_HTML)
            template = ezt.Template(f.name, compress_whitespace=0)
            os.unlink(f.name)
        fp = io.StringIO()
        template.generate(fp, metadata)
        content = fp.getvalue()
        return content, metadata


def add_reader(readers):
    readers.reader_classes['emd'] = ASFReader


def register():
    signals.readers_init.connect(add_reader)
