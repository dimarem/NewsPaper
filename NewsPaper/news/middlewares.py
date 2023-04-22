import pytz

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')

        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()

        return self.get_response(request)


class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session['theme']:
            hour = timezone.now().hour
            request.session['theme'] = 'dark' if hour > 19 or hour < 7 else 'light'

        return self.get_response(request)
