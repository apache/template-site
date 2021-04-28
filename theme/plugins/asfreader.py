"""
asfreader.py
----------------
Pelican plugin that processes Markdown files through as an ezt template then through GitHub Flavored Markdown.
"""

import os.path
import sys
import io
import re
import ezt

from tempfile import NamedTemporaryFile

from pelican import signals
from pelican.utils import pelican_open
import pelican.readers

GFMReader = sys.modules['pelican-gfm.gfm'].GFMReader

class ASFReader(GFMReader):
    enabled = True
    file_extensions = ['ezmd', 'emd']

    def read(self, source_path):
        "Read metadata and content, process content as ezt template, then render into HTML."

        # read content with embedded ezt
        text, metadata = super().read_source(source_path)
        assert text
        assert metadata
        # supplement metadata with ASFData
        print("ASF Data file: %s" % self.settings.get("ASF_DATA", ()))
        # write ezt content to temporary file
        with NamedTemporaryFile(delete=False) as f:
            if sys.version_info >= (3, 0):
                text = text.encode('utf-8')
            f.write(text)
            f.close()
            # prepare ezt content as ezt template
            template = ezt.Template(f.name, compress_whitespace=0, base_format=ezt.FORMAT_HTML)
            assert template
            os.unlink(f.name)
            # generate content from ezt template with metadata
            fp = io.StringIO()
            template.generate(fp, metadata)
            text = fp.getvalue()
            # Render the markdown into HTML
            if sys.version_info >= (3, 0):
                text = text.encode('utf-8')
                content = super().render(text).decode('utf-8')
            else:
                content = super().render(text)
            assert content

        return content, metadata


# def add_readers(readers):
#    readers.reader_classes['ezmd'] = ASFReader


def register():
    print("ASFReader registered")
#    pelican.plugins.signals.readers_init.connect(add_readers)
