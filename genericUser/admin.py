from django.contrib import admin

# Register your models here.
from genericUser.models import *

admin.site.register(Announcement)
admin.site.register(BannerContent)
admin.site.register(DisabilityCard)
admin.site.register(Organization)
admin.site.register(QAndA)
admin.site.register(RecommendationSubject)
admin.site.register(ServiceInfo)
admin.site.register(User)
