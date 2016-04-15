# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User)
    itn = models.CharField(max_length=12)
    ammount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return '%s %s' % (self.user.username, self.itn)
