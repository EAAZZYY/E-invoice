from django.db import models
from django.utils import timezone

# Create your models here.

class BusinessProfile(models.Model):
    business_name = models.CharField(max_length=200)
    registered = models.BooleanField()
    registration_number = models.CharField(max_length=200)
    business_line = models.IntegerField()
    business_email = models.EmailField()
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField()
    
    def save(self,*args, **kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, BusinessProfile).save(*args, **kwargs)
        
    def __str__(self):
        return self.business_name
    
class AccountDetail(models.Model):
    business_name = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=200)
    account_name = models.CharField(max_length=200)
    account_number = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField()
    
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
    edited_on = models.DateTimeField()
    
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, CustomerProfile).save(*args, **kwargs)
    
    def __str__(self):
        return self.customer_name
    
class ProductService(models.Model):
    product_name = models.CharField(max_length=200)
    price_per_unit = models.DecimalField()
    product_quantity = models.IntegerField
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField()
    
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, ProductService).save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name

class Invoice(models.Model):
    business_name = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    invoice_title = models.CharField(max_length=200)
    products = models.ForeignKey(ProductService, on_delete=models.CASCADE)
    sub_total = models.IntegerField()
    tax_rate = models.IntegerField()
    grand_total = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField()
    
    def save(self,*args,**kwargs):
        if self.edited_on == "None":
            self.edited_on = timezone.localtime(timezone.now())
        return super(self, Invoice).save(*args, **kwargs)
    
    def __str__(self):
        return self.invoice_title
