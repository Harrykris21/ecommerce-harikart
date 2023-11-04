# custommiddleware.py

class FontProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for a font file (e.g., .woff2, .ttf)
        if request.path.startswith('/fonts'):
            request.META['HTTP_X_SCRIPT_NAME'] = '/fastkart/assets/fonts'
        return self.get_response(request)
