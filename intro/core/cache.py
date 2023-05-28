from django.core.cache import cache


def cache_otp(name, code):
    cached_data = cache.set(name, code, timeout=3000)
    return cached_data


def get_cached_otp(name):
    cached_otp = cache.get(name)
    return cached_otp
