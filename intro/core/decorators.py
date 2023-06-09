from django.utils.translation import activate
from functools import wraps


def user_language(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        language = request.headers['Accept-Language']
        activate(language)
        return func(request, *args, **kwargs)
    return wrapper
