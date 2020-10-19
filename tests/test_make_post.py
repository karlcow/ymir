import pytest

from tests.utils import get_fixture_path
from tests.utils import read_text_fixture
from ymir.utils import make_post


def test_parsing_meta():
    """We get the meta data and the text."""
    doc = read_text_fixture('draft-meta.md')
    post_meta, post_text = make_post.parse(doc)
    assert post_meta == {'date': '2020-10-19',
                         'prev': '/2020/10/18/',
                         'style': '/2020/style',
                         'title': 'Titre',
                         'url': 'somewhere'}
    assert post_text == 'Some text'