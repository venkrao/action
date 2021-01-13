from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Coach)
admin.site.register(CourseSubcategory)
admin.site.register(CourseCategory)
admin.site.register(Language)
admin.site.register(SessionPackageOffering)
admin.site.register(ActioSession)

admin.site.register(AmazonResourceName)
admin.site.register(TwilioRoom)