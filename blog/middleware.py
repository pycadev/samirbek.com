import time
from django.utils.deprecation import MiddlewareMixin

class PerformanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            # X-Response-Time header for debug
            response['X-Response-Time'] = str(int(duration * 1000)) + "ms"
            
            # Simple way to pass to template via cookie or context (using cookie for simplicity in SSR)
            response.set_cookie('perf_time', str(int(duration * 1000)))
        return response
