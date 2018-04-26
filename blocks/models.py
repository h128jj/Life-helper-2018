from django.db import models

# Create your models here.


class Block(models.Model):
    name = models.CharField(u"Block name", max_length=100)
    desc = models.CharField(u"Block desc", max_length=100)
    post_nums = models.IntegerField(u"Post nums", default=0)
    posts = models.CharField(u"Block posts", max_length=1000000, default="0")
    status = models.IntegerField("Status", choices=((1, "exist"), (0, "deleted")), default=0)
    # created_date = models.DateTimeField("Created Date", default=timezone.now())
    # modified_date = models.DateTimeField("Modified Date", default=timezone.now())
    # created_date = models.CharField("Created Date", max_length=100, default=str(datetime.now())[:-7])
    # modified_date = models.CharField("Modified Date", max_length=100, default=str(datetime.now())[:-7])
    create_timestamp = models.DateTimeField("Created Timestamp", auto_now_add=True)
    update_timestamp = models.DateTimeField("Last Update Timestamp", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Block name"
        verbose_name_plural = "Blocks"
