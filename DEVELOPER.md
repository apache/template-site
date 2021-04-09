# Web Developer Guide

We are using [GitHub Flavored Markdown](https://github.github.com/gfm/).

JavaScript frameworks available are:

- [JQuery 3.6.0 Slim](https://code.jquery.com/jquery-3.6.0.slim.js)
- [Popper 1.14.7](https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.js)
- [Bootstrap 4.3.1](https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.js)

CSS frameworks available are:

- [Bootstrap 4.3.1](https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.css)
- [GitHub Markdown 3.0.1](https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/3.0.1/github-markdown.css)

Additional testing with GitHub Actions:

- [Lint](.github/workflows/lint.yml) -- [GitHub Actions](https://docs.github.com/en/actions) Workflow
- [Flake8](https://flake8.pycqa.org/en/latest/) - [Python](https://www.python.org/) based tool for style guide enforcement
- [markdownlint](https://github.com/DavidAnson/markdownlint) -- using [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) - [Node.js](https://nodejs.org/) style checker and lint tool for [Markdown](https://daringfireball.net/projects/markdown/) and CommonMark files
- [misspell](https://github.com/client9/misspell) -- [Golang](https://golang.org/) library to correct commonly misspelled English words quickly
- [yamllint](https://yamllint.readthedocs.io/en/stable/) -- a linter for [YAML](https://yaml.org/) files

For misspell you can pass in `-w` to autocorrect misspelled words. You can also autocorrect some markdownlint
errors by using the `--fix` flag.

Developer Tools:

- [EditorConfig](https://editorconfig.org/) -- helps maintain consistent coding styles for multiple developers working on the same project across various editors and IDEs
- [GNU Midnight Commander](http://midnight-commander.org/) -- is a free cross-platform orthodox file manager. It was started by Miguel de Icaza in 1994 as a clone of the then-popular Norton Commander. GNU Midnight Commander is part of the GNU project and is licensed under the terms of the GNU General Public License

IDEs that some contributors to Petri use:

- [Atom](https://atom.io/) -- At GitHub, we’re building the text editor we’ve always wanted: hackable to the core, but approachable on the first day without ever touching a config file. We can’t wait to see what you build with it
- [GNU Emacs](https://www.gnu.org/software/emacs/) -- An extensible, customizable, free/libre text editor — and more. At its core is an interpreter for Emacs Lisp, a dialect of the Lisp programming language with extensions to support text editing
- [GNU nano](https://www.nano-editor.org/) -- a text editor for Unix-like computing systems or operating environments using a command line interface. It emulates the Pico text editor, part of the Pine email client, and also provides additional functionality. Unlike Pico, nano is licensed under the GNU General Public License. Released as free software by Chris Allegretta in 1999, nano became part of the GNU Project in 2001
- [IntelliJ IDEA Community](https://www.jetbrains.com/idea/) -- Every aspect of IntelliJ IDEA has been designed to maximize developer productivity. Together, intelligent coding assistance and ergonomic design make development not only productive but also enjoyable
- [Sublime Text](https://www.sublimetext.com/) -- Sublime Text is a sophisticated text editor for code, markup and prose. You'll love the slick user interface, extraordinary features and amazing performance
- [Vim](https://www.vim.org/) -- a highly configurable text editor built to make creating and changing any kind of text very efficient. It is included as "vi" with most UNIX systems and with Apple macOS

Useful Git tools:

- [GitHub Desktop](https://desktop.github.com/) -- Simple collaboration from your desktop
- [GitKraken](https://www.gitkraken.com/) -- Free Git GUI for Windows, Mac, Linux
- [Git GUI Clients](https://git-scm.com/downloads/guis)
- [gitk](https://git-scm.com/docs/gitk) -- The Git repository browser
- [git-gui](https://git-scm.com/docs/git-gui) -- A portable graphical interface to Git
- [gitg](https://gitlab.gnome.org/GNOME/gitg) -- a graphical user interface for git
- [GitHub CLI](https://cli.github.com/) -- Take GitHub to the command line. GitHub CLI brings GitHub to your terminal. Free and open source

Test your website:

- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) -- Sharing Debugger lets you preview how your content will look when it's shared to Facebook and debug any issues with your Open Graph tags
- [Favicon checker](https://realfavicongenerator.net/favicon_checker) -- Is your favicon perfect? Let us give a look. We check more than a dozen settings to make sure it fits all major platforms
- [Google Rich Results Test](https://search.google.com/test/rich-results) -- Rich results are experiences on Google surfaces, such as Search, that go beyond the standard blue link. Rich results can include carousels, images or other non-textual elements
- [GTmetrix](https://gtmetrix.com/) -- See how your site performs, reveal why it's slow and discover optimization opportunities
- [Help Search Engines Understand Your Website](https://www.opengraph.xyz/) -- Preview and Generate Open Graph Meta Tags
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) -- Lighthouse is an open-source, automated tool for improving the quality of web pages. You can run it against any web page, public or requiring authentication. It has audits for performance, accessibility, progressive web apps, SEO and more
- [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly) -- Test how easily a visitor can use your page on a mobile device. Just enter a page URL to see how your page scores
- [Nu HTML Checker](https://validator.w3.org/nu/)
- [PageSpeed Insights](https://developers.google.com/speed/pagespeed/insights/) -- Make your web pages fast on all devices
- [Pingdom Website Speed Test](https://tools.pingdom.com/) -- Enter a URL to test the page load time, analyze it, and find bottlenecks
- [REDbot](https://redbot.org/) -- REDbot is lint for HTTP resources; it tests protocol correctness, cacheability, content negotiation and more
- [Twitter Cards Validator](https://cards-dev.twitter.com/validator)
- [W3C Feed Validation Service](https://validator.w3.org/feed/) -- Free service that checks the syntax of Atom or RSS feeds
- [W3C Markup Validation Service](https://validator.w3.org/)
- [WebPageTest](https://www.webpagetest.org/) -- Test. Optimize. Repeat
