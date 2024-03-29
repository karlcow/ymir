from datetime import datetime
from glob import glob
import locale
from pprint import pprint
import re
import sys
from textwrap import dedent

import mistune
from PIL import Image


ROOT = '/Users/karl/Sites/la-grange.net'
INDENTATION = re.compile(r'\n\s{2,}')
META = re.compile(r'^(\w+):([^\n]*)\n')
PATH = re.compile(r'^.*(\d{4})/(\d{2})/(\d{2})/.*')
TEMPLATE = """date: {date}
prev: {prev}
title: {title}
url: {url}
style: /2019/style
"""


class GrangeRenderer(mistune.HTMLRenderer):
    """Adjusted renderer for La Grange."""
    def get_img_size(self, image_path):
        """extract width and height of an image."""
        full_path = ROOT + image_path
        try:
            with Image.open(full_path) as im:
                return im.size
        except FileNotFoundError as e:
            print('TOFIX: Image file path incorrect')
            sys.exit(f'       {e}')

    def image(self, src, alt="", title=None):
        width, height = self.get_img_size(src)
        if title:
            return dedent(f"""
                <figure>
                  <img src="{src}"
                       alt="{alt}"
                       width="{width}" height="{height}" />
                  <figcaption>{title}</figcaption>
                </figure>
                """)
        else:
            s = f'<img src="{src}" alt="{alt}" width="{width}" height="{height}" />'  # noqa
            return s

    def paragraph(self, text):
        # In case of a figure, we do not want the (non-standard) paragraph.
        # david larlet's code idea
        if text.strip().startswith("<figure>"):
            return text
        return f"<p>{text}</p>\n"


def parse(text):
    """Parse the given text into metadata and strip it for a Markdown parser.
    :param text: text to be parsed
    """
    rv = {}
    m = META.match(text)

    while m:
        key = m.group(1)
        value = m.group(2)
        value = INDENTATION.sub('\n', value.strip())
        if not value:
            sys.exit("ERROR: Some meta are missing")
        rv[key] = value
        text = text[len(m.group(0)):]
        m = META.match(text)
    return rv, text.lstrip()


def get_draft(entry_path):
    """Read the draft.

    It returns a tuple with:
    - meta: dict
    - text: str
    """
    try:
        with open(entry_path) as entry:
            text = entry.read()
    except FileNotFoundError as e:
        print('TOFIX: draft file path incorrect')
        sys.exit(f'       {e}')
    else:
        return parse(text)

def add_id(html_text):
    """Post process to add certain ids."""
    # Add id to links section
    html_text = html_text.replace(
        '<h2>sur le bord du chemin</h2>',
        '<h2 id="links">sur le bord du chemin</h2>')
    return html_text

def main():
    """Main workflow."""
    locale.setlocale(locale.LC_ALL, 'fr_FR')
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)

    p = parser.parse_args()
    entry_path = p.file_path
    template_path = f'{ROOT}/2019/12/04/article_tmpl.html'
    with open(template_path) as tmpfile:
        blog_tmp = tmpfile.read()
    # Read the draft post
    meta, markdown_text = get_draft(entry_path)
    pprint(meta)
    prev_url = meta['prev']
    # Read the previous blog entry
    with open(ROOT + prev_url + '.html') as prev_entry:
        from bs4 import BeautifulSoup
        text_prev = prev_entry.read()
        htmldata = BeautifulSoup(text_prev, features="lxml")
        prev_title = htmldata.find('title').text
        prev_title = prev_title.replace(' - Carnets Web de La Grange', '')
    # Meta extraction
    # Created
    created_timestamp = '{datestr}T23:59:59+09:00'.format(datestr=meta['date'])
    d = datetime.fromisoformat(meta['date'])
    day = d.day
    day_path = f"{d:%d}"
    year = d.year
    month = f"{d:%m}"
    month_name = f"{d:%B}"
    # special rendering
    renderer = GrangeRenderer()
    markdown = mistune.create_markdown(
        renderer=renderer, plugins=['strikethrough'], escape=False)
    html_text = markdown(markdown_text)
    # Post processing of markdown text
    html_text = add_id(html_text)
    # metadata
    metadata = {
        'title': meta['title'],
        'created_timestamp': created_timestamp,
        'day': day,
        'year': year,
        'month': month,
        'month_name': month_name,
        'updated_timestamp': created_timestamp,
        'updated': meta['date'],
        'prev_url': meta['prev'],
        'prev_title': prev_title,
        'post_text': html_text,
        'day_path': day_path,
        'url': meta['url'],
        'stylepath': meta['style'],
        }
    blog_post = blog_tmp.format(**metadata)
    dest = ROOT + '/{year}/{month}/{day_path}/{url}.html'.format(**metadata)
    print(dest)
    with open(dest, 'w') as blogpost:
        blogpost.write(blog_post)


def extract_date(path):
    full_date = PATH.match(path)
    return '-'.join(full_date.groups())


if __name__ == "__main__":
    main()
