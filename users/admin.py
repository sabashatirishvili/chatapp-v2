from django.contrib import admin
from .models import *
from django.contrib import admin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
  pass

admin.site.register(User, UserAdmin)