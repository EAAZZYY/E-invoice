from django.db import models

from django.utils.text import slugify
from uuid import uuid4

from django.utils import timezone

from django.conf import settings


# Create your models here.
"""
Business Schema
"""
class BusinessProfile(models.Model):
    business_name = models.CharField(max_length=200)
    business_line = models.CharField(max_length=20, blank=True, null=True)
    business_email = models.EmailField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    last_edited_on = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["-created_on"]
    
    def save(self,*args, **kwargs):
        if self.last_edited_on == "None":
            self.last_edited_on = timezone.localtime(timezone.now())
        return super(BusinessProfile, self ).save(*args, **kwargs)
        
    def __str__(self):
        return self.business_name


"""
Customer Schema
"""    
class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone_number = models.CharField(max_length=20, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    last_edited_on = models.DateTimeField(blank=True, null=True)
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name="business")
    
    class Meta:
        ordering = ["-created_on"]
    
    def save(self,*args,**kwargs):
        if self.last_edited_on == "None":
            self.last_edited_on = timezone.localtime(timezone.now())
        return super(Customer, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.customer_name


"""
Invoice Schema
"""
class Invoice(models.Model):
    invoice_name = models.CharField(max_length=200)
    invoice_slug = models.SlugField(max_length=200, blank=True, null=True)
    invoice_number = models.CharField(max_length=200, blank=True, null=True, unique=True)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    created_on = models.DateField(auto_now=True)
    last_edited_on = models.DateTimeField(blank=True, null=True)
    business_name = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["-created_on"]
    
        
    def save(self,*args,**kwargs):
        if self.last_edited_on == "None":
            self.last_edited_on = timezone.localtime(timezone.now())
        
        if not self.invoice_slug:
            self.invoice_slug = slugify(self.invoice_name)
            
        if not self.invoice_number:
            self.invoice_number = str(uuid4()).split("-")[0]
        
        return super(Invoice, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.invoice_name
    

"""
Invoice Item Schema
"""
class Item(models.Model):
    item_name = models.CharField(max_length=200)
    item_quantity = models.IntegerField()
    item_price = models.IntegerField(blank=True, null=True)
    item_total = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    last_edited_on = models.DateTimeField(blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE )
    
    def save(self,*args,**kwargs):
        if self.last_edited_on == "None":
            self.last_edited_on = timezone.localtime(timezone.now())
        return super(Item, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.item_name