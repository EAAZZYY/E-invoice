from django.urls import path
from . import views

app_name = "invoice"

urlpatterns = [
    # Url routes for landing page, business, customer and invoice list views
    path('',views.homeview,name='home'),
    path('business_list/',views.business_list,name='business'),
    path('customers_list/',views.customer_list, name="customer_list"),
    path('invoice_list/',views.InvoiceListView.as_view(), name='invoice_list'),
    
    # Url routes for business, customer and invoice forms views
    path('create_business/',views.add_business, name='add_business'),
    path('create_customers/', views.create_customer, name='create_customer'),
    path('create_invoice/',views.create_invoice, name='create_invoice'),
    
    # Url routes for invoice detail and delete for invoice, customer and business views
    path('invoice_detail/<slug:slug>', views.invoice_detail,name='invoice_detail'),
    path('delete_invoice/<slug:slug>/', views.invoice_delete,name='delete_invoice'),
    path('delete_customer/<int:id>', views.delete_customer,name='delete_customer'),
    path('delete_business/<int:id>/', views.delete_business, name='delete_business'),
    
    # Url route for pdf convert view
    path('pdf_convert/<slug:slug>', views.pdf_convert,name='pdf_convert')
]
