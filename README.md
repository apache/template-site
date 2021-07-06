# Apache Template

[Apache Template](https://template.staged.apache.org/)

This repository provides a website template for [ASF-Pelican](https://infra.apache.org/asf-pelican.html)

Pelican build site infrastructure is found [here](https://github.com/apache/infrastructure-pelican)

If you use this template for your project website and provide a [logo](https://www.apache.org/logos/) then
your project should pass "[Apache Project Website Checks](https://whimsy.apache.org/site/)".

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
   - [`asfdata.yaml`](asfdata.yaml) has many examples

4. Edit your [configuration](pelicanconf.yaml)
   - Site specific information
   - Theme path
   - Plugin configuration. If you develop your own plugin or pull in plugins via pip then be sure to include it in `use:`
   - Setup is used to add data models, shell scripts, ignored files and directories, and any special copy action.
   - Genid invokes various special features including elementid and headingid with permalinks, table of contents, table class,
     and enabling of "unsafe" html.

5. Create your [content](content)
   - `.md` files using Github Flavored Markdown ([**gfm**](https://infra.apache.org/gfm.html))
   - `.ezmd` files for templates using `ASF_DATA`

6. Building
   - [Local build instructions](https://infra.apache.org/asf-pelican-local.html)
   - [ASF YAML build](.asf.yaml) -- [ASF infrastructure instructions](https://cwiki.apache.org/confluence/display/INFRA/git+-+.asf.yaml+features)

7. [Suggested Branch Strategy](https://infra.apache.org/asf-pelican-branches.html)

8. [Issues and Template Questions](https://github.com/apache/template-site/issues)

9. Tools
   - [GitHub Actions](https://docs.github.com/en/actions)
     - [Lint manual workflow](.github/workflows/lint.yml)
   - [EditorConfig](https://editorconfig.org/) -- helps maintain consistent coding styles for multiple developers working on
     the same project across various editors and IDEs
     - [.editorconfig](.editorconfig)
