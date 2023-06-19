import requests
from zeep.client import Client

from django.conf import settings

client = Client(settings.ZARINPAL['sandbox']['ZARINPAL_REQUEST_URL'])


class ZarinpalRequest:
    """ Zarinapl Request Configuration and sender """

    # Zarinpal Sandbox information configuration
    DEBUG_ZARINPAL_REQUEST_URL = settings.ZARINPAL['sandbox']['ZARINPAL_REQUEST_URL']
    DEBUG_ZARINPAL_AUTHORITY_URL = settings.ZARINPAL['sandbox']['ZARINPAL_AUTHORITY_URL']
    DEBUG_MERCHANT_ID = settings.ZARINPAL['sandbox']['MERCHANT_ID']
    DEBUG_ZARINPAL_VERIFY_URL = settings.ZARINPAL['sandbox']['ZARINPAL_VERIFY_URL']
    DEBUG_CALLBACK_URL = settings.ZARINPAL['sandbox']['CALLBACK_URL']
    # Zarinpal RealWorld information configuration
    ZARINPAL_REQUEST_URL = settings.ZARINPAL['default']['ZARINPAL_REQUEST_URL']
    ZARINPAL_AUTHORITY_URL = settings.ZARINPAL['default']['ZARINPAL_AUTHORITY_URL']
    MERCHANT_ID = settings.ZARINPAL['default']['MERCHANT_ID']
    ZARINPAL_VERIFY_URL = settings.ZARINPAL['default']['ZARINPAL_VERIFY_URL']
    CALLBACK_URL = settings.ZARINPAL['default']['CALLBACK_URL']

    def __init__(self):
        if settings.DEBUG:
            self.request_url = self.DEBUG_ZARINPAL_REQUEST_URL
            self.authority_url = self.DEBUG_ZARINPAL_AUTHORITY_URL
            self.verify_url = self.DEBUG_ZARINPAL_VERIFY_URL
            self.merchant_id = self.DEBUG_MERCHANT_ID
            self.callback = self.DEBUG_CALLBACK_URL
        else:
            self.request_url = self.ZARINPAL_REQUEST_URL
            self.authority_url = self.ZARINPAL_AUTHORITY_URL
            self.verify_url = self.ZARINPAL_VERIFY_URL
            self.merchant_id = self.MERCHANT_ID
            self.callback = self.CALLBACK_URL

    def send_real_request(self, amount, description, phone, email):
        data = {
            'merchant_id': self.merchant_id,
            'callback_url': self.callback,
            'amount': amount,
            'phone': phone,
            'email': email,
            'description': description
        }
        # sending data to zarinpal
        resp = requests.post(self.request_url, data=data)
        if resp.status_code == 200:
            authority = resp.json()['Authority']
            return authority
        print(resp.json())
        return False

    def send_real_verify_request(self, amount, authority):
        data = {
            'merchant_id': self.merchant_id,
            'amount': amount,
            'authority': authority
        }
        # Sending request to zarinpal verify url
        resp = requests.post(self.verify_url, data=data)
        # checking results
        if resp.status_code == 200:
            resp = resp.json()
            if resp["Status"] == 100 or resp["Status"] == 101:
                return resp["RefID"]
            print(resp)
            return resp
        print(resp)
        return False

    def send_sandbox_request(self, amount, description="test transaction",
                             email="test@gmail.com", phone="09123456789"):
        result = client.service.PaymentRequest(self.merchant_id, amount,
                                               description, email, phone, self.callback)
        if result.Status == 100:
            return result.Authority
        return False

    def send_sandbox_verify_request(self, authority, amount):
        result = client.service.PaymentVerification(self.merchant_id, authority, amount)
        if result.Status == 100 or result.Status == 101:
            return result.RefID
        return False

    def send_request(self, amount, description, email, phone):
        if settings.DEBUG:
            return self.send_sandbox_request(amount, description, email, phone)
        return self.send_real_request(amount, description, phone, email)

    def send_verify(self, amount, authority):
        if settings.DEBUG:
            return self.send_sandbox_verify_request(authority, amount)
        return self.send_real_verify_request(amount, authority)


zarinpal = ZarinpalRequest()
