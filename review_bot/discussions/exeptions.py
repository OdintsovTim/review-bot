class WebhookError(Exception):
    pass


class WebhookTokenError(WebhookError):
    pass


class WebhookDataError(WebhookError):
    pass
