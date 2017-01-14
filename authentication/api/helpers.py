import datetime
import random
import re

from django.contrib.auth.models import User


def generate_username():
    condition = True
    while(condition):
        generated_username = _generate_string()

        response = User.objects.filter(username__startswith=generated_username).order_by('-id')
        if not response:
            generated_username += '0'
        else:
            get_last_user_registered = response[0]
            count = re.findall(r'\d+', str(get_last_user_registered))[0]
            generated_username += str(int(count) + 1)

        try:
            User.objects.get(username=generated_username)
        except User.DoesNotExist:
            condition = False

    return generated_username


def _generate_string():
    """Auto generate string according to date"""
    prefix = "self_"

    date = datetime.datetime.utcnow()
    date_year = date.year
    date_month = date.month
    date_day = date.day

    if date_day > 26:
        date_month = date_month + 12
        date_day = date_day - 26

    part = chr(date_year + 97 - 2014) + \
        chr(97 + date_month - 1) + chr(97 + date_day - 1)

    generated_string = prefix + part

    return generated_string


def generate_password():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ()#$^&"
    password_len = 8
    password = ""
    for i in range(password_len):
        next_index = random.randrange(len(alphabet))
        password += alphabet[next_index]
    return password
