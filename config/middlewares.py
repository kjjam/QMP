from django.http.response import HttpResponseNotFound

from config import settings


def block_non_json_request(get_response):
    """
    block the request with content-type not application/json
    In settings.ALLOWED_JSON_URLS you can add exception to pass reeuest.
    """

    def middleware(request):
        base_url = request.path[1:].split("/")[0]
        if request.content_type != "application/json":
            if base_url not in settings.ALLOWED_JSON_URLS:
                return HttpResponseNotFound()
        response = get_response(request)
        return response

    return middleware
