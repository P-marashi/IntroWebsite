from django.core.cache import cache


def cache_otp(name, code):
    """ Helper function for caching otp  """
    cached_data = cache.set(name, code, timeout=120000)
    return cached_data


def get_cached_otp(name):
    """ Helper function for getting cached otp """
    cached_otp = cache.get(name)
    return cached_otp
