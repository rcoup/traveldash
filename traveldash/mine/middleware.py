class SeenHttpReferer(object):
    """
    Tracks whether we've ever seen a non-empty HTTP Referer header
    in this session.
    """
    def process_request(self, request):
        if request.META.get('HTTP_REFERER', ''):
            request.session['seen_http_referer'] = True
