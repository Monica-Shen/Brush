from django.db import models


class Account(models.Model):
    account_id = models.CharField(max_length=8)
    account_pass = models.CharField(max_length=16)
    account_email = models.CharField(max_length=25, default='')


class WebPage(models.Model):
    webPage_pageid = models.CharField(max_length=10)
    webPage_widget = models.CharField(max_length=1024, default='')
    webPage_account_id = models.CharField(max_length=8)
