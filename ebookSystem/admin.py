from django.contrib import admin


# Register your models here.
from django.contrib.auth.admin import UserAdmin
from ebookSystem.models import *
from genericUser.models import *

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookInfo)
admin.site.register(EBook)
admin.site.register(Organization)
admin.site.register(ServiceInfo)
admin.site.register(EditRecord)
admin.site.register(EditLog)
admin.site.register(GetBookRecord)
admin.site.register(BookOrder)
admin.site.register(LibraryRecord)
admin.site.register(Announcement)
admin.site.register(BannerContent)
admin.site.register(RecommendationSubject)
admin.site.register(QAndA)
admin.site.register(DisabilityCard)
admin.site.register(BusinessContent)
admin.site.register(Category)
admin.site.register(IndexCategory)
