from django.contrib import admin


# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *
from account.models import *
from genericUser.models import *
from guest.models import *

admin.site.register(User)
admin.site.register(Editor)
admin.site.register(Guest)
admin.site.register(Book)
admin.site.register(EBook)
admin.site.register(ContactUs)
admin.site.register(Reply)
admin.site.register(Event)
admin.site.register(ReviseContentAction)
