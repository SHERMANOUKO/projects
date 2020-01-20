from django.db import models
from datetime import datetime, timedelta

# Create your models here.

# this could include many models

# i use only two tables for demonstration


# default to 90 days from now
def get_default_my_date():
    return datetime.now() + timedelta(days=90)

class Accounts(models.Model):
    accountID = models.AutoField(primary_key=True)
    accountEmail = models.EmailField()
    accountHolderName = models.CharField(max_length=255)
    accountExpiryDate = models.DateTimeField(default=get_default_my_date)

class ExpiredAccounts(models.Model):
    id = models.AutoField(primary_key=True)
    accountEmail = models.EmailField(unique=True)