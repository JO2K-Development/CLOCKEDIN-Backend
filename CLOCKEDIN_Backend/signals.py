# from allauth.socialaccount.signals import social_account_added
# from allauth.socialaccount.signals import social_account_updated
# from allauth.account.signals import user_signed_up
# from allauth.account.signals import user_logged_in
# from django.dispatch import receiver
#
# @receiver(user_signed_up)
# def update_user_attributes(sender, request, user, **kwargs):
#     print("triggered4")
#     if user.temporary:
#         # Update user attributes here
#         user.temporary = False
#         user.save()
#
# @receiver(user_logged_in)
# def update_user_attributes(sender, request, user, **kwargs):
#     print("triggered3")
#     if user.temporary:
#         # Update user attributes here
#         user.temporary = False
#         user.save()
#
# @receiver(social_account_updated)
# def update_user_attributes(sender, request, sociallogin, **kwargs):
#     print("triggered2")
#     user = sociallogin.user
#     if user.temporary:
#         # Update user attributes here
#         user.temporary = False
#         user.save()
#
#
# @receiver(social_account_added)
# def update_user_attributes(sender, request, sociallogin, **kwargs):
#     print("triggered1")
#     user = sociallogin.user
#     if user.temporary:
#         # Update user attributes here
#         user.temporary = False
#         user.save()