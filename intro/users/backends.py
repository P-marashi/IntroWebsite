from django.contrib.auth import get_user_model
from django.db.models import Q


class EmailOrPhoneNumber:
    @staticmethod
    def authenticate(request, email, phone_number, password):
        try:
            user = get_user_model().objects.get(
                 Q(phone_number=phone_number) | Q(email=email)
            )

        except get_user_model().DoesNotExist:
            return None 

        if user and user.check_password(password):
            return user

        return None
