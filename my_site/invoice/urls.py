from django.urls import path
from . import views

app_name = "invoice"

urlpatterns = [
    path('',views.HomeListView.as_view(),name='home'),
    path('invoice_list/',views.InvoiceListView.as_view(), name='invoice_list'),
    path('create_business/',views.AddBusinessView.as_view(), name='add_business'),
    path('create_customers/', views.CustomerCreateView.as_view(), name='create_customer'),
    path('create_invoice/',views.InvoiceCreateView.as_view(), name='create_invoice'),
    path('invoice_detail/<slug:slug>', views.invoicedetail,name='invoice_detail'),
    path('customer_detail/<int:id>', views.customerdetail,name='customer_detail')
]
