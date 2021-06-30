import json
from json import JSONDecodeError
from typing import Mapping

from django.http import HttpRequest

from review_bot.discussions.models import WebhookSecretToken, Comment, Discussion, Developer, Commit, Project
from review_bot.discussions.exeptions import WebhookTokenError, WebhookDataError


class GitlabCommentService:
    @classmethod
    def handle_request(cls, request: HttpRequest):
        cls._check_webhook_token(request)
        json_comment_data = cls._get_data_from_request(request)

        #  So far, we do not handle cases when the comment is written outside the code
        if not json_comment_data['object_attributes']['line_code']:
            return

        project = cls._get_project(json_comment_data)
        commit_author = cls._get_commits_author(json_comment_data)
        commit = cls._get_commit(json_comment_data, commit_author, project)

        developer = cls._get_developer(json_comment_data)
        discussion = cls._get_discussion(json_comment_data, developer, commit)

        cls._save_comment_to_db(json_comment_data, discussion, developer, commit)

    @classmethod
    def _check_webhook_token(cls, request: HttpRequest) -> None:
        if not request.META.get('X-Gitlab-Token'):
            raise WebhookTokenError('X-Gitlab-Token not set')

        webhook_secret_tokens = WebhookSecretToken.objects.values_list('secret_token', flat=True)
        if request.META.get('X-Gitlab-Token') not in webhook_secret_tokens:
            raise WebhookTokenError('X-Gitlab-Token is incorrect')

    @classmethod
    def _get_data_from_request(cls, request: HttpRequest) -> Mapping:
        try:
            json_comment_data = json.loads(request.body.decode())
        except (UnicodeDecodeError, JSONDecodeError):
            raise WebhookDataError('Incorrect input data format')

        if not isinstance(json_comment_data, dict):
            raise WebhookDataError('Parsed object type from incoming data is not a dictionary')

        return json_comment_data

    @classmethod
    def _get_project(cls, json_comment_data: Mapping) -> Project:
        try:
            project, _ = Project.objects.get_or_create(
                project_id=json_comment_data['project_id'],
                defaults={
                    'name': json_comment_data['project']['name'],
                    'default_branch': json_comment_data['project']['default_branch'],
                    'web_url': json_comment_data['project']['web_url'],
                },
            )
        except KeyError:
            raise WebhookDataError("Request data doesn't contain info about project")

        return project

    @classmethod
    def _get_developer(cls, json_comment_data: Mapping) -> Developer:
        try:
            developer, _ = Developer.objects.get_or_create(
                email=json_comment_data['user']['email'],
                name=json_comment_data['user']['name'],
            )
        except KeyError:
            raise WebhookDataError("Request data doesn't contain info about developer")

        return developer

    @classmethod
    def _get_commits_author(cls, json_comment_data: Mapping) -> Developer:
        try:
            commit_author, _ = Developer.objects.get_or_create(
                email=json_comment_data['commit']['author']['email'],
                name=json_comment_data['user']['author']['name'],
            )
        except KeyError:
            raise WebhookDataError("Request data doesn't contain info about commit author")

        return commit_author

    @classmethod
    def _get_commit(cls, json_comment_data: Mapping, commit_author: Developer, project: Project) -> Commit:
        try:
            commit, _ = Commit.objects.get_or_create(
                commit_id=json_comment_data['commit']['id'],
                defaults={
                    'created_at': json_comment_data['commit']['timestamp'],
                    'title': json_comment_data['commit']['title'],
                    'web_url': json_comment_data['commit']['url'],
                    'project': project,
                    'developer': commit_author,
                },
            )
        except KeyError:
            raise WebhookDataError("Request data doesn't contain info about commit")

        return commit

    @classmethod
    def _get_discussion(cls, json_comment_data: Mapping, developer: Developer, commit: Commit) -> Discussion:
        try:
            discussion, created = Discussion.objects.get_or_create(
                discussion_id=json_comment_data['discussion_id'],
                defaults={
                    'author': developer,
                    'commit': commit,
                },
            )
        except KeyError:
            raise WebhookDataError("Request data doesn't contain info about discussion")

        if not created:
            discussion.participants.add(developer)

        return discussion

    @classmethod
    def _save_comment_to_db(
        cls,
        json_comment_data: Mapping,
        discussion: Discussion,
        developer: Developer,
        commit: Commit,
    ) -> None:
        try:
            Comment.objects.get_or_create(
                comment_id=json_comment_data['object_attributes']['id'],
                defaults={
                    'note': json_comment_data['object_attributes']['note'],
                    'created_at': json_comment_data['object_attributes']['created_at'],
                    'author': developer,
                    'commit': commit,
                    'discussion': discussion,
                },
            )
        except KeyError:
            raise WebhookDataError("Request data doesn't contain info about comment")
