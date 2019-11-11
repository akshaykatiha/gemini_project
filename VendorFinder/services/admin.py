from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import VendorForm, CustomerForm
from .models import (
    User,
    Vendor,
    Customer,
    Admin,
    Service,
    SubService,
    Status,
    VendorService,
    Invoice
)

admin.site.register(User, UserAdmin)
admin.site.register(Vendor)
admin.site.register(Customer)
admin.site.register(Admin)
admin.site.register(Service)
admin.site.register(SubService)
admin.site.register(Status)
admin.site.register(VendorService)
admin.site.register(Invoice)
#admin.site.register()