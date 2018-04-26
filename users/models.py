from django.db import models
from datetime import datetime, timedelta


# Create your models here.


class User(models.Model):
    email = models.CharField('Email', max_length=30)
    password = models.CharField('Password', max_length=20)
    nickname = models.CharField('Nickname', max_length=20)
    posts = models.CharField('Posts', max_length=10000, default='')
    stevens_id = models.CharField('Stevens ID', max_length=8)
    is_Verified = models.BooleanField('Is verified', default=False)
    is_Admin = models.BooleanField('Is admin', default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"


class UserActive(models.Model):
    user = models.ForeignKey(User, verbose_name='User ID', on_delete=models.PROTECT)
    active_code = models.CharField('Active Code', max_length=50)
    expire_date = models.CharField('Expire date', max_length=50,
            auto_created=(datetime.today()+timedelta(days=1)).strftime("%Y-%m-%d"))
    is_expired = models.BooleanField("Is expired", default=False)

    def __str__(self):
        return self.active_code

    class Meta:
        verbose_name = "Active ID"
        verbose_name_plural = "Active ID"


