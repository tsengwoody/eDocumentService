from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Editor)
admin.site.register(Guest)
admin.site.register(Book)
admin.site.register(EBook)
