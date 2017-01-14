from django.db import models


class Verification(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    secret_identifier = models.CharField(max_length=48, blank=True)
    expiry = models.DateTimeField(null=True)

    def __str__(self):
        return self.phone


class Mapping(models.Model):
    phone = models.CharField(max_length=10, unique=True)
    access_token_granted = models.BooleanField(default=False)
    alias = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.phone
