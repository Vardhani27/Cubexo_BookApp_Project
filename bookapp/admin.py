from django.contrib import admin

from bookapp.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Books)
admin.site.register(OTPforRegistration)