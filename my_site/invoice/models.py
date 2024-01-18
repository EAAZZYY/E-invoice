from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.

class BusinessProfile(models.Model):
    business_name = models.CharField(max_length=200)
    business_line = models.IntegerField()
    business_email = models.EmailField()
    created_on = models.DateTimeField(auto_now=True)
    last_edited_on = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def save(self,*args, **kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, BusinessProfile).save(*args, **kwargs)
        
    def __str__(self):
        return self.business_name
    
class AccountDetail(models.Model):
    bank_name = models.CharField(max_length=200)
    account_name = models.CharField(max_length=200)
    account_number = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True)
    last_edited_on = models.DateTimeField()
    business_name = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, AccountDetail).save(*args,**kwargs)
    
    def __str__(self):
        return f"{self.business_name.business_name}'s account details"
    
class CustomerProfile(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone_number = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True)
    last_edited_on = models.DateTimeField()
    
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, CustomerProfile).save(*args, **kwargs)
    
    def __str__(self):
        return self.customer_name


class Invoice(models.Model):
    invoice_title = models.CharField(max_length=200)
    invoice_number = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField()
    business_name = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, Invoice).save(*args, **kwargs)
    
    def __str__(self):
        return self.invoice_title
    

class InvoiceItem(models.Model):
    item_name = models.CharField(max_length=200)
    item_quantity = models.IntegerField()
    item_price = models.DecimalField()
    item_total = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField()
    
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, InvoiceItem).save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name

class InvoiceTotal(models.Model):
    sub_total = models.IntegerField()
    tax_rate = models.DecimalField()
    grand_total = models.DecimalField()
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, InvoiceItem).save(*args, **kwargs)
