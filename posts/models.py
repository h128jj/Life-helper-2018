from django.db import models
from blocks.models import Block
from users.models import User
from datetime import datetime

# Create your models here.


class Post(models.Model):
    block = models.ForeignKey(Block, verbose_name="Block Name", on_delete=models.PROTECT)
    title = models.CharField("Title", max_length=100)
    content = models.CharField("Content", max_length=10000)
    status = models.IntegerField("Status", choices=((1, "exist"), (0, "deleted")), default=0)
    picture = models.CharField("Picture", max_length=30000, blank=True)
    create_timestamp = models.DateTimeField("Created Timestamp", auto_now_add=True)
    update_timestamp = models.DateTimeField("Last Update Timestamp", auto_now=True)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.PROTECT)
    author_name = models.CharField('Author Name', max_length=100)
    desc = models.CharField('Description', max_length=10000)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Post"