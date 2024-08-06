from django.contrib.auth import get_user_model
import re


def email_validator(email):
    email_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if re.fullmatch(email_regex_pattern, email):
        check_email = get_user_model().objects.filter(email=email)
        if not check_email:
            return True
    return False


def password_validator(pswd):
    if pswd and len(pswd) >= 6:
        return True
    return False


def username_validator(username):
    if username and len(username) >= 3:
        return True
    return False