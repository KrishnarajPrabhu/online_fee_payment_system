from django.shortcuts import redirect
from django.conf import settings


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path_info
        print(path)

        if request.path == settings.LOGIN_URL or request.path == '/validation/' or request.path == '/stu/paymenthandler/':
            return self.get_response(request)

        elif request.path != settings.LOGIN_URL:
            if self.is_authenticated(request):
                return self.get_response(request)
            else:
                return redirect('/login/')

    def is_authenticated(self, request):
        return request.session.get('logged_in')
