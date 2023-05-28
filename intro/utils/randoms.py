import string
import hashlib
import random
import base64


class RandomGenerator:
    def __init__(self, encode_to_base64=False, hash=False):
        self.random_string = None
        self.encode = encode_to_base64
        self.hash = hash

    def encode_base64(self, data):
        if self.encode:
            return base64.b64encode(data.encode()).decode()
        elif self.hash:
            return hashlib.md5(data.encode()).hexdigest()
        return data

    def generate_unique_hash(self):
        rand_lowercase = [
            random.choice(string.ascii_lowercase) for x in range(6)
        ]
        rand_uppercase = [
            random.choice(string.ascii_uppercase) for x in range(6)
        ]
        rand_digits = [
            random.choice(string.digits) for x in range(6)
        ]
        rand = rand_uppercase + rand_lowercase + rand_digits
        return self.encode_base64(rand)
