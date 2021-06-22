import pytest


@pytest.fixture
def gitlab_commit():
    return {
        'id': '45fc959da6e06cd53324dbf1fa69f504f6b088d8',
        'short_id': '45fc959d',
        'created_at': '2021-06-22T17:36:15.000+03:00',
        'parent_ids': ['04cce141181c7eeec9335326dce72bce28b1bf6f4'],
        'title': 'Very useful commit',
        'message': 'Very useful commit\n',
        'author_name': 'dev123',
        'author_email': 'dev123@zipsale.co.uk',
        'authored_date': '2021-06-22T17:36:15.000+03:00',
        'committer_name': 'dev123',
        'committer_email': 'dev123@zipsale.co.uk',
        'committed_date': '2021-06-22T17:36:15.000+03:00',
        'trailers': {},
        'web_url': 'https://gitlab.com/group/project/-/commit/45fc959da6e06cd53324dbf1fa69f504f6b088d8',
    }
