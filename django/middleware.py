from django.utils.deprecation import MiddlewareMixin
import json


class ParseAppjsonMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.content_type == 'application/json':
            try:
                request._post = json.loads(request.body)
            except Exception:
                pass