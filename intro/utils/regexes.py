# TODO: Add regexes
import re

PHONE_NUMBER_REGEX = r""
EMAIL_REGEX = r""


def is_phone_or_email(method):
    """ Check given data is phone number or email address
    ...
    Args:
    -----
    method: str
    it should be phonenumber or email address
    Returns:
    --------
    str-> "phone" | "email"
    bool-> False 
    when condition is False the False value will return
    """
    if re.match(PHONE_NUMBER_REGEX, method):
        return "phone"
    elif re.match(EMAIL_REGEX, method):
        return "email"
    return False
