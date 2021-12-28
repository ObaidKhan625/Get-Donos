from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Donation_made)
admin.site.register(Donation_Request)