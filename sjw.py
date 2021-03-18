#!/usr/bin/env python

import os
from pathlib import Path
import re
import sys

import argparse

# for exception
import jinja2

from markdown import Markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from staticjinja import Site

# Set up argparse
def init_argparse():
    parser = argparse.ArgumentParser(description='Generate HTML pages from Markdown wiki pages.')
    parser.add_argument('--dir', '-d', required=True, help='directory containing Markdown wiki pages')
    return parser

markdown = Markdown(output_format="html5", extensions=[WikiLinkExtension(base_url='', end_url='.html')])

def md_context(template):
    markdown_content = Path(template.filename).read_text()
    return {"post_content_html": markdown.convert(markdown_content)}

def render_md(site, template, **kwargs):
    # mangle the name the same way WikiLinkExtension does
    clean_name = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', template.name)
    out = site.outpath / Path(clean_name).with_suffix(".html")

    # compile and stream the result
    os.makedirs(out.parent, exist_ok=True)
    site.get_template(str(Path() / ".staticjinjawiki" / "page.html")).stream(**kwargs).dump(str(out), encoding="utf-8")

def main():
    argparser = init_argparse();
    args = argparser.parse_args();

    try:
        site = Site.make_site(
            searchpath=args.dir,
            outpath=str(Path() / args.dir / ".staticjinjawiki" / "output"),
            contexts=[(r".*\.md", md_context)],
            rules=[(r".*\.md", render_md)],
        )
        site.render()

    except jinja2.exceptions.TemplateNotFound as err:
        sys.stderr.write("\nMissing template. Please create file: {}\n\n".format(err))
        sys.exit(1)

if __name__ == "__main__":
    exit(main())
