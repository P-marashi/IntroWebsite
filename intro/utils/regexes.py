# TODO: Add regexes
import re

PHONE_NUMBER_REGEX = \
    r"[\+\d]?(\d{2,3}[-\.\s]??\d{2,3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
EMAIL_REGEX = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"


def is_phone_or_email(method):
    """ Check given data is phone number or email address
    ...
    Args:
    -----
    method: str
    it should be phonenumber or email address
    Returns:
    --------
    str -> "phone" | "email"
    bool -> False
    when condition is False the False value will return
    """
    if re.match(PHONE_NUMBER_REGEX, method):
        return "phone"
    elif re.match(EMAIL_REGEX, method):
        return "email"
    return False
