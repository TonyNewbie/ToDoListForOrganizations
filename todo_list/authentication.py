from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Organization


# Custom authentication scheme by email and check user organization
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, organization=None, **kwargs):
        # Use custom user model
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
            organization = Organization.objects.get(name=organization)
            if user.check_password(password) and organization in user.organizations.all():
                return user
            return None
        except User.DoesNotExist:
            return None
