import random


@property
def otp_generator():
    """ generate a random 5 length otp code """
    return random.randrange(10000, 99999)
