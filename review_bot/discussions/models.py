from django.db import models


class Project(models.Model):
    project_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    default_branch = models.CharField(max_length=100)
    web_url = models.SlugField(max_length=150)

    def __str__(self):
        return f'{self.name}'


class Developer(models.Model):
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=50)
    slack_id = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.name}'


class Commit(models.Model):
    commit_id = models.CharField(max_length=50)
    short_id = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField()
    title = models.CharField(max_length=200)
    web_url = models.SlugField(max_length=200)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='commits')
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='commits')


class Discussion(models.Model):
    discussion_id = models.PositiveIntegerField()
    author = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='discussions')
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE, related_name='discussions')
    participants = models.ManyToManyField(Developer, blank=True)


class Comment(models.Model):
    comment_id = models.PositiveIntegerField()
    note = models.TextField()
    created_at = models.DateTimeField()
    author = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='comments')
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE, related_name='comments')
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments')


class WebhookSecretToken(models.Model):
    secret_token = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='webhook_secret_tokens')
