from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from review_bot.discussions.exeptions import WebhookError
from review_bot.discussions.services.comment import GitlabCommentService


@method_decorator(csrf_exempt, name='dispatch')
class GitlabWebhookView(View):
    def post(self, request: HttpRequest):
        try:
            GitlabCommentService.handle_request(request)
        except WebhookError:
            #  need to log
            return HttpResponseBadRequest

        return HttpResponse
