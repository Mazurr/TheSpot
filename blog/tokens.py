from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccountActivationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationToken()

class PasswordResetToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp)
        )

password_reset_token = PasswordResetToken()