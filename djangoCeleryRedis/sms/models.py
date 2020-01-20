from django.db import models

# Create your models here.
# this could include many models

# i use only one table for demonstration
class ScheduledDispatch(models.Model):
    dispatchID = models.AutoField(primary_key=True)
    dispatchRecipient = models.IntegerField()
    dispatchItem = models.CharField(max_length=255)