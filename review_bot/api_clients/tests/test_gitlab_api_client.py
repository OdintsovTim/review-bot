from json import JSONDecodeError

import pytest
import responses
from django.conf import settings
from requests.exceptions import ConnectionError

from review_bot.api_clients.gitlab import GitlabApiClient


@responses.activate
def test_make_request(gitlab_commit):
    endpoint = 'commits'
    responses.add(
        responses.GET,
        f'https://gitlab.com/api/{settings.GITLAB_API_VERSION}/{endpoint}/',
        json=[gitlab_commit],
        status=200,
    )

    response = GitlabApiClient._make_request(endpoint, skip_parsing_result=False)

    assert response == [gitlab_commit]


@pytest.mark.parametrize(
    'body, status_code',
    [
        (ConnectionError, 200),
        (JSONDecodeError, 200),
        ('not found', 404),
    ],
)
@responses.activate
def test_make_request_raise_errors(body, status_code):
    responses.add(
        responses.GET,
        'https://gitlab.com/api/',
        body=body,
        status=status_code,
    )

    assert GitlabApiClient._make_request() is None
