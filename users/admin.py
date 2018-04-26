from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'nickname', 'stevens_id', 'is_Verified', 'is_Admin']

admin.site.register(User, UserAdmin)