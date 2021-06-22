from typing import TypedDict, Mapping


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
