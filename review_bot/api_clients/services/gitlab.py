import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Mapping

import pytz
from django.conf import settings

from review_bot.api_clients.custom_types import GitlabCommitData
from review_bot.api_clients.gitlab import GitlabApiClient
from review_bot.review.models import Project, Commit, Developer


class GitlabService:
    def __init__(self, group_id: int) -> None:
        self.group_id: int = group_id

    @staticmethod
    def _add_project_webhook_with_comment_events(project_id: int) -> None:
        token: str = str(uuid.uuid4())
        GitlabApiClient.add_project_webhook_with_comment_events(project_id, token)

    @staticmethod
    def _save_group_projects_to_db(projects: list[Mapping]) -> list[int]:
        new_projects_ids: list[int] = []

        for project in projects:
            _, created = Project.objects.get_or_create(
                project_id=project['id'],
                defaults={
                    'name': project['name'],
                    'default_branch': project['default_branch'],
                    'web_url': project['web_url'],
                },
            )

            if created:
                new_projects_ids.append(project['id'])

        return new_projects_ids

    @staticmethod
    def _fetch_commits_for_the_last_day(project_id: int) -> list[GitlabCommitData]:
        local_today = datetime.now(tz=pytz.timezone(settings.REVIEW_TIMEZONE))
        local_yesterday = local_today - timedelta(days=1)
        start_time_utc = local_yesterday.replace(hour=0, minute=0, second=0, microsecond=0).astimezone(timezone.utc)
        end_time_utc = local_yesterday.replace(hour=23, minute=59, second=59, microsecond=999).astimezone(timezone.utc)
        start_time_string = start_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')
        end_time_string = end_time_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')

        return GitlabApiClient.fetch_commits(project_id, since=start_time_string, until=end_time_string)

    @staticmethod
    def _save_commits_to_db(commits: list[GitlabCommitData], project_id: int) -> None:
        for commit in commits:
            project: Project = Project.objects.get(project_id=project_id)
            developer, _ = Developer.objects.get_or_create(
                email=commit['committer_email'],
                name=commit['committer_name'],
            )

            Commit.objects.get_or_create(
                commit_id=commit['id'],
                defaults={
                    'short_id': commit['short_id'],
                    'title': commit['title'],
                    'web_url': commit['web_url'],
                    'project': project,
                    'developer': developer,
                    'created_at': commit['committed_date'],
                },
            )

    def synchronize_projects(self) -> None:
        projects: Optional[list[Mapping]] = self._fetch_group_projects()
        if projects is None:
            return

        new_projects_ids = self._save_group_projects_to_db(projects)
        for new_project_id in new_projects_ids:
            self._add_project_webhook_with_comment_events(new_project_id)

    def synchronize_commits_for_the_last_day(self) -> None:
        project_ids = Project.objects.values_list('project_id', flat=True)

        for project_id in project_ids:
            commits = self._fetch_commits_for_the_last_day(project_id)

            self._save_commits_to_db(commits, project_id)

    def synchronize_all_data(self):
        self.synchronize_projects()
        self.synchronize_commits_for_the_last_day()

    def _fetch_group_projects(self) -> Optional[list[Mapping]]:
        return GitlabApiClient.fetch_group_projects(self.group_id)
