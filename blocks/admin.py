from django.contrib import admin
from .models import Block
# Register your models here.


class BlockAdmin(admin.ModelAdmin):
    list_display = ("name", "desc", "post_nums", "status")

admin.site.register(Block, BlockAdmin)