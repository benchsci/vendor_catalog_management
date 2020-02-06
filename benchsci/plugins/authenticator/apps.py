from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured


class AuthenticatorConfig(AppConfig):
    name = 'benchsci.plugins.authenticator'

    def ready(self):
        from django.conf import settings

        settings.INSTALLED_APPS += ["social_django"]
        settings.AUTHENTICATION_BACKENDS = (
            "social_core.backends.open_id.OpenIdAuth",
            "social_core.backends.google.GoogleOpenId",
            "social_core.backends.google.GoogleOAuth2",
            "django.contrib.auth.backends.ModelBackend",
        )
        settings.SOCIAL_AUTH_URL_NAMESPACE = "social"
        settings.SOCIAL_AUTH_PIPELINE = (
            "social.pipeline.social_auth.social_details",
            "social.pipeline.social_auth.social_uid",
            "social.pipeline.social_auth.auth_allowed",
            "social.pipeline.social_auth.social_user",
            "social.pipeline.user.get_username",
            "social.pipeline.user.create_user",
            "social.pipeline.social_auth.associate_user",
            "social.pipeline.debug.debug",
            "social.pipeline.social_auth.load_extra_data",
            "social.pipeline.user.user_details",
            "social.pipeline.debug.debug",
        )
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]
        settings.TEMPLATES[0]["OPTIONS"]["context_processors"] += [
            "social_django.context_processors.backends",
            "social_django.context_processors.login_redirect",
        ]

        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = settings.BENCHSCI_AUTHENTICATOR_OAUTH_KEY
        settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = settings.BENCHSCI_AUTHENTICATOR_OAUTH_SECRET

        # Raise exception if these are not set in settings.py
        settings.LOGIN_URL
        settings.LOGOUT_REDIRECT_URL
