# TODO: Add regexes
import re

PHONE_NUMBER_REGEX = r""
EMAIL_REGEX = r""


def is_phone_or_email(method):
    if re.match(PHONE_NUMBER_REGEX, method):
        return "phone"
    elif re.match(EMAIL_REGEX, method):
        return "email"
    return False
