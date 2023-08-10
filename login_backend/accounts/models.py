from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=100)
    user_position = models.CharField(max_length=100)

    class Meta:
        app_label = 'accounts'