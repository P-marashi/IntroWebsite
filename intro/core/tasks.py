from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail


OTP_CONTENT = """{name} عزیز!
به وبسایت {website_name} خوش اومدی!

کد ورود شما به وبسایت: {otp_code}

ممنون از اینکه مارو انتخاب کردید.
"""


@shared_task
def send_otp_mobile():
    # TODO: OTP Service code will place here
    return 1


@shared_task
def send_otp_email(to_email, otp_code):
    return send_mail(subject=f"کد ورود به {settings.SITE_NAME}", message="",
              html_message=OTP_CONTENT.format(name=to_email,
                    website_name=settings.SITE_NAME, otp_code=otp_code),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[to_email])
