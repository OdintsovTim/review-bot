from django.contrib import admin

from review_bot.review.models import Developer, Discussion, Project, Commit, Comment


admin.site.register(Developer)
admin.site.register(Discussion)
admin.site.register(Project)
admin.site.register(Commit)
admin.site.register(Comment)