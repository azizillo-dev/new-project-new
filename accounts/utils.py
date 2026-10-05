import re

phone_regex = re.compile(r'^\+998\d{9}$')
email_regex = re.compile(r'^[\w.+-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$')

def get_auth_type(value):
    value = value.strip()
    if phone_regex.fullmatch(value):
        return 'phone'
    elif email_regex.fullmatch(value):
        return 'email'
    else:
        return None




    