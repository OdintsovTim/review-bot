from json import JSONDecodeError
from typing import Union, Optional

import requests
from django.conf import settings
from tenacity import retry, stop_after_attempt, TryAgain
from requests import Response

from review_bot.api_clients.base import BaseApiClient
from review_bot.api_clients.custom_types import GitlabCommitData


class GitlabApiClient(BaseApiClient):
    @classmethod
    def fetch_commits(
        cls,
        project_id: int,
        since: str = None,
        until: str = None,
        per_page: int = 100,
    ) -> Optional[list[GitlabCommitData]]:
        endpoint: str = f'projects/{project_id}/repository/commits/'
        params: dict = {'since': since, 'until': until, 'per_page': per_page}

        return cls._make_request(endpoint, params=params)

    @classmethod
    def _make_paginated_request(
        cls,
        endpoint: str = None,
        params=None,
    ) -> Optional[list]:
        response = cls._make_request(endpoint, params=params)
        if response is None:
            return None

        response_data = response.json()
        next_page = response.headers.get('X-Next-Page')

        for _ in range(settings.GITLAB_MAX_PAGINATOR_DEPTH):
            if next_page is not None:
                params['page'] = next_page
                next_page_response = cls._make_request(endpoint, params=params)
                if next_page_response is None:
                    return response_data

                response_data += next_page_response.json()
                next_page = response.headers.get('X-Next-Page')
            else:
                break

        return response_data

    @classmethod
    @retry(
        stop=stop_after_attempt(5),
        retry_error_callback=lambda retry_state: None,
    )
    def _make_request(
        cls,
        endpoint: str = None,
        method: str = 'get',
        json_data=None,
        params=None,
        skip_parsing_result: bool = True,
    ) -> Union[Response, list, None]:
        url = f'https://gitlab.com/api/{settings.GITLAB_API_VERSION}/{endpoint}/'
        method_kwargs = {
            'url': url,
            'headers': {'Authorization': f'Bearer {settings.GITLAB_PRIVATE_TOKEN}'},
            'params': params,
        }

        if json_data:
            method_kwargs['json'] = json_data

        try:
            response = getattr(requests, method)(**method_kwargs)
        except ConnectionError:
            # need to log
            raise

        if not response.ok:
            # need to log
            raise TryAgain

        try:
            return response if skip_parsing_result else response.json()
        except JSONDecodeError:
            # need to log
            raise