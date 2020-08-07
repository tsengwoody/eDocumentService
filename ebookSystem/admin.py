from django.contrib import admin


# Register your models here.
from ebookSystem.models import *

admin.site.register(Book)
admin.site.register(BookInfo)
admin.site.register(EBook)
admin.site.register(EditRecord)
admin.site.register(EditLog)
admin.site.register(GetBookRecord)
admin.site.register(BookOrder)
admin.site.register(LibraryRecord)
admin.site.register(Category)
admin.site.register(IndexCategory)
