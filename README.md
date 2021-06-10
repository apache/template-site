# Apache Template

[Apache Template](https://template.staged.apache.org/)

This repository provides a website template for [ASF-Pelican](https://infra.apache.org/asf-pelican.html)

## How to use this template

1. Ask Infra to **Use this template** to create your new site repository

2. Update the theme's `base.html` to fit your site's requirements
   - [Theme](theme/apache/templates) -- example template
     The example has the following frameworks.
     - JavaScript:
       - [JQuery 3.6.0 Slim](https://code.jquery.com/jquery-3.6.0.slim.js)
       - [Popper 1.14.7](https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.js)
       - [Bootstrap 4.3.1](https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.js)
     - CSS:
       - [Bootstrap 4.3.1](https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.css)
       - [GitHub Markdown 3.0.1](https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/3.0.1/github-markdown.css)
     For fenced code hightlighting have a look at [highlightjs](https://highlightjs.org)
   - [Images](content/images) -- example logo and other images

3. Determine if your site requires a [data model](https://infra.apache.org/asf-pelican-data.html).
   - The `.ezmd` files in the [content](content) directory show examples
   - [`asfdata.yaml`](asfdata.yaml) has manuy examples
   - Remove the following if you do not need a data model:
     1. `asfdata.py` and `asfreader.py` [Plugins](/theme/plugins)
     2. `asfdata.yaml`
     3. `data` directory

4. Edit your [configuration](pelicanconf.py)
   - Website specific
   - `PLUGINS`
   - `ASF_DATA` - `asfdata.py` plugin settings
   - `ASF_GENID` - `asfgenid.py` plugin settings
     `asfgenid.py` performs a series of html fixups including permalinks, heading ids, and table of contents

5. Create your [content](content)
   - `.md` files using Github Flavored Markdown ([**gfm**](https://infra.apache.org/gfm.html)
   - `.ezmd` files for templates using `ASF_DATA`

6. Building
   - [Local build instructions](https://infra.apache.org/asf-pelican-local.html)
   - [ASF YAML build](.asf.yaml) -- ASF infrastructure instructions

7. [Suggested Branch Strategy](https://infra.apache.org/asf-pelican-branches.html)

8. [Issues and Template Questions](https://github.com/apache/template-site/issues)

9. Tools
   - [GitHub Actions](https://docs.github.com/en/actions)
     - [Lint manual workflow](.github/workflows/lint.yml)
   - [EditorConfig](https://editorconfig.org/) -- helps maintain consistent coding styles for multiple developers working on
     the same project across various editors and IDEs
     - [.editorconfig](.editorconfig)
