from django.contrib import admin
from .models import BusinessProfile, AccountDetail, CustomerProfile, Invoice, Item

# Register your models here.
admin.site.register(BusinessProfile)
admin.site.register(AccountDetail)
admin.site.register(CustomerProfile)
admin.site.register(Invoice)
admin.site.register(Item)