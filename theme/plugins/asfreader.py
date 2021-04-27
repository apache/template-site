"""
asfreader.py
----------------
Pelican plugin that processes Markdown files through as an ezt template then through GitHub Flavored Markdown.
"""

import os
import sys
import io
import re
import ezt

from tempfile import NamedTemporaryFile

from pelican import signals
from pelican.utils import pelican_open
import pelican.readers

GFMReader = sys.modules['pelican-gfm.gfm']

class ASFReader(GFMReader):
    # Note: name starts in column 0, no whitespace before colon, will be
    #       made lower-case, and value will be stripped
    #
    RE_METADATA = re.compile('^([A-za-z]+): (.*)$')

    def read_source(self, source_path):
        # Prepare the "slug", which is the target file name. It will be the
        # same as the source file, minus the leading ".../content/(articles|pages)"
        # and with the extension removed (Pelican will add .html)
        relpath = os.path.relpath(source_path, self.settings['PATH'])
        parts = relpath.split(os.sep)
        parts[-1] = os.path.splitext(parts[-1])[0]  # split off ext, keep base
        slug = os.sep.join(parts[1:])
        print(slug)

        metadata = {
            'slug': slug,
            'part0': parts[0]
        }
        # Fetch the source content, with a few appropriate tweaks
        with pelican.utils.pelican_open(source_path) as text:

            # Extract the metadata from the header of the text
            lines = text.splitlines()
            for i in range(len(lines)):
                line = lines[i]
                match = RE_METADATA.match(line)
                if match:
                    name = match.group(1).strip().lower()
                    if name != 'slug':
                        value = match.group(2).strip()
                        if name == 'date':
                           value = pelican.utils.get_date(value)
                    metadata[name] = value
                    #if name != 'title':
                    #  print 'META:', name, value
                elif not line.strip():
                    # blank line
                    continue
                else:
                    # reached actual content
                    break

            # Reassemble content, minus the metadata
            text = '\n'.join(lines[i:])
            if sys.version_info >= (3, 0):
                text = text.encode('utf-8')

            return text, metadata

    def read(self, source_path):
        print(source_path)
        # read content with embedded ezt
        text, metadata = self.read_source(source_path)
        # supplement metadata with ASFData
        # print(self.settings.get("ASF_DATA", ()))
        # write ezt content to temporary file
        template = None
        content = None
        with NamedTemporaryFile(delete=False) as f:
            f.write(text)
            f.close()
            # prepare ezt content as ezt template
            template = ezt.Template(f.name, compress_whitespace=0, base_format=ezt.FORMAT_HTML)
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

            # Redo the slug for articles.
            # depending on pelicanconf.py this will change the output filename
            if metadata['part0'] == 'articles' and 'title' in metadata:
                metadata['slug'] = pelican.utils.slugify(
                    metadata['title'],
                    self.settings.get('SLUG_SUBSTITUTIONS', ()))

        return content, metadata


def add_readers(readers):
    readers.reader_classes['emd'] = ASFReader


def register():
    pelican.plugins.signals.readers_init.connect(add_readers)
