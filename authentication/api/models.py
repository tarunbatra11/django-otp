from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    """
    Store additional user data.
    """
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.user.username
