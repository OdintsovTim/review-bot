from django.db import models


class Project(models.Model):
    project_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    default_branch = models.CharField(max_length=100)
    web_url = models.SlugField(max_length=150)


class Developer(models.Model):
    gitlab_id = models.PositiveIntegerField()
    email = models.EmailField()
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    slack_id = models.PositiveIntegerField()


class Commit(models.Model):
    commit_id = models.CharField(max_length=50)
    short_id = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    title = models.CharField(max_length=200)
    web_url = models.SlugField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='commits')
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='commits')


class Discussion(models.Model):
    is_opened = models.BooleanField(default=True)
    author = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='discussions')


class Comment(models.Model):
    note = models.TextField()
    created_at = models.DateTimeField()
    line = models.IntegerField()
    author = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='comments')
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE, related_name='comments')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')