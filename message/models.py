from django.db import models
from users.models import User
from datetime import datetime

# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(User, verbose_name="User id", on_delete=models.PROTECT)
    post_title = models.CharField("Post Title", max_length=1000)
    replier = models.CharField("Replier", max_length=100)
    content = models.CharField("Content", max_length=10000)
    link = models.CharField("Link", max_length=10000)
    status = models.IntegerField("Status", choices=((1, "Unread"), (0, "Read")), default=1)
    create_date = models.CharField('Create date', max_length=50,
                                   auto_created=(datetime.today()).strftime("%Y-%m-%d"))
