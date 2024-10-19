import logging

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

logger = logging.getLogger(__name__)

from django.db import IntegrityError

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        try:
            user = super().save_user(request, sociallogin, form)

            # Validate and set foreign keys
            if not user.company:
                user.company = None  # or raise an error if company is required

            if not user.manager:
                user.manager = None  # or raise an error if manager is required

            user.temporary = True
            user.save()

        except IntegrityError as e:
            logger.error(f"Foreign key constraint error: {e}")
            raise

        return user
