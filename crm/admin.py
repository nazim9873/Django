from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Enquiry)
admin.site.register(Registration)
admin.site.register(Payment)
admin.site.register(EnquiryFollowup)
