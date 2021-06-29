from typing import TypedDict, Mapping, Optional


class GitlabCommitData(TypedDict):
    id: str  # noqa: A003, VNE003
    short_id: str
    created_at: str
    parent_ids: list[str]
    title: str
    message: str
    author_name: str
    author_email: str
    authored_date: str
    committer_name: str
    committer_email: str
    committed_date: str
    trailers: Mapping
    web_url: str


class GitlabWebhookData(TypedDict):
    id: int  # noqa: A003, VNE003
    url: str
    created_at: str
    push_events: bool
    tag_push_events: bool
    merge_requests_events: bool
    repository_update_events: bool
    enable_ssl_verification: bool
    project_id: int
    issues_events: bool
    confidential_issues_events: bool
    note_events: bool
    confidential_note_events: Optional[bool]
    pipeline_events: bool
    wiki_page_events: bool
    deployment_events: bool
    job_events: bool
    releases_events: bool
    push_events_branch_filter: Optional[str]


class GitlabUserData(TypedDict):
    id: int  # noqa: A003, VNE003
    name: str
    username: str
    state: str
    avatar_url: str
    created_at: str
    bio: str
    bio_html: str
    location: str
    public_email: str
    skype: str
    linkedin: str
    twitter: str
    website_url: str
    organization: str
    job_title: str
    pronouns: Optional[str]
    bot: bool
    work_information: Optional[str]
    followers: str
    following: str
