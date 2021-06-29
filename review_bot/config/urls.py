from django.conf import settings
from django.contrib import admin
from django.urls import path

from review_bot.discussions.views import GitlabWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
]
