from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.db import IntegrityError


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        try:
            # Call the default save logic
            user = super().save_user(request, sociallogin, form)

            # Handle foreign keys or custom fields as needed
            if not user.company:
                user.company = None  # Or set a default valid company, if required

            if not user.manager:
                user.manager = None  # Or handle as None if no manager exists

            # Set other custom fields if needed
            user.temporary = True  # Set default value for custom field

            # Save the user with updated fields
            user.save()

        except IntegrityError as e:
            # Log the error for debugging
            print(f"IntegrityError during user save: {e}")
            raise

        return user
