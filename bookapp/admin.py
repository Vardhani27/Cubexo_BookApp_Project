from django.contrib import admin

from bookapp.models import *

# Register your models here.
admin.site.register(AppUserRole)
admin.site.register(Book)
admin.site.register(OTPforRegistration)