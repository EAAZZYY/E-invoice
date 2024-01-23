from django.urls import path
from . import views

app_name = "invoice"

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('business_list/',views.BusinessListView.as_view(),name='business'),
    path('invoice_list/',views.InvoiceListView.as_view(), name='invoice_list'),
    path('create_business/',views.AddBusinessView.as_view(), name='add_business'),
    path('create_customers/', views.CustomerCreateView.as_view(), name='create_customer'),
    path('create_invoice/',views.InvoiceCreateView.as_view(), name='create_invoice'),
    path('invoice_detail/<slug:slug>', views.invoicedetail,name='invoice_detail'),
    path('delete_invoice/<slug:slug>/', views.invoicedelete,name='delete_invoice'),
    path('delete_customer/<int:id>', views.deletecustomer,name='delete_customer'),
    path('delete_business/<int:id>/', views.deletebusiness, name='delete_business')
]
