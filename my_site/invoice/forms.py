from django import forms

from django.forms import inlineformset_factory

from .models import BusinessProfile, Customer, Invoice, Item

"""
For BusinessProfile and Customer Forms,
ModelForm was used. 

For Invoice and Item Forms
Inlineformset_Factory was used.
In line with DRY principle
"""

""" ModelForms"""
class BusinessForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = ['business_name','business_line','business_email']


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['business','customer_name','customer_email', 'customer_phone_number']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_name','business_name','customer_name','grand_total']


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_quantity', 'item_price','item_total']


"""
Inlineformset_factory form
"""
InvoiceItemFormSet = inlineformset_factory(Invoice,Item,form=InvoiceItemForm,extra=10)