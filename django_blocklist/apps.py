from django.apps import AppConfig


class Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_blocklist"
    defaults = {
        "cooldown": 7,
        "denial-template": "Your IP address {ip} has been blocked. Try again in {cooldown} days.",
        }
