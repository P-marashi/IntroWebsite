import random


@property
def otp_generator():
    return random.randrange(10000, 99999)
