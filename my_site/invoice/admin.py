from django.contrib import admin

from .models import BusinessProfile, Customer, Invoice

"""
Registering models for interaction on the backend
"""
# Register your models here.
admin.site.register(BusinessProfile)
admin.site.register(Customer)
admin.site.register(Invoice)
