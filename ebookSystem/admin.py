from django.contrib import admin


# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *
from account.models import *
from genericUser.models import *
from guest.models import *

admin.site.register(User)
admin.site.register(Guest)
admin.site.register(Book)
admin.site.register(BookInfo)
admin.site.register(EBook)
admin.site.register(Event)
admin.site.register(Organization)
admin.site.register(ServiceInfo)
admin.site.register(EditRecord)
admin.site.register(EditLog)
admin.site.register(Article)