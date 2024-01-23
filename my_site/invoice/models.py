from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from uuid import uuid4
# Create your models here.

class BusinessProfile(models.Model):
    business_name = models.CharField(max_length=200)
    business_line = models.IntegerField(blank=True, null=True)
    business_email = models.EmailField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    last_edited_on = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def save(self,*args, **kwargs):
        if self.last_edited_on == "None":
            self.last_edited_on = timezone.localtime(timezone.now())
        return super(BusinessProfile, self ).save(*args, **kwargs)
        
    def __str__(self):
        return self.business_name

    
class CustomerProfile(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone_number = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
    last_edited_on = models.DateTimeField(blank=True, null=True)
    
    def save(self,*args,**kwargs):
        if self.last_edited_on == "None":
            self.last_edited_on = timezone.localtime(timezone.now())
        return super(CustomerProfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.customer_name


class Invoice(models.Model):
    invoice_name = models.CharField(max_length=200)
    invoice_slug = models.SlugField(max_length=200, blank=True, null=True)
    invoice_number = models.CharField(max_length=200, blank=True, null=True, unique=True)
    grand_total = models.DecimalField(max_digits=15, decimal_places=2,blank=True,null=True)
    created_on = models.DateField(auto_now=True)
    last_edited_on = models.DateTimeField(blank=True, null=True)
    business_name = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    
        
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