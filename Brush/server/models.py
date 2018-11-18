from django.db import models


class Account(models.Model):
    account_id = models.CharField(max_length=8)
    account_pass = models.CharField(max_length=16)




