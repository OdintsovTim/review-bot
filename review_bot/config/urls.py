from django.conf import settings
from django.contrib import admin
from django.urls import path

from review_bot.discussions.views import GitlabWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(settings.GITLAB_WEBHOOK_URL, GitlabWebhookView.as_view(), name='gitlab_webhook'),
]
