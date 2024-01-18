from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from . import forms

from . import models

# Create your views here.

class HomeListView(ListView):
    model = models.CustomerProfile
    context_object_name = 'customers'
    template_name = 'invoice/home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        business_profile = models.BusinessProfile.objects.filter(user=self.request.user)
        
        context['businesses'] = business_profile
        context['account_detail'] = models.AccountDetail.objects.filter(business_profile__in=business_profile)
        return context
    
class InvoiceListView(ListView):
    model = models.Item
    template_name = 'invoice/invoice_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        business_profile = models.BusinessProfile.objects.filter(user=self.request.user)
        invoices = models.Invoice.objects.filter(business_name__in = business_profile)
        context['invoices'] = invoices
        return context

def invoicedetail(request, slug):
    invoice = models.Invoice.objects.get(invoice_slug=slug)
    # invoice_items = invoice.invoice_set.all()
    return render(request, 'invoice/invoice_detail.html', context={'invoice':invoice})


def customerdetail(request, id):
    customer = models.CustomerProfile.objects.get(id=id)
    # invoice_items = invoice.invoice_set.all()
    return render(request, 'invoice/customer_detail.html', context={'customer':customer})

    
class CustomerCreateView(CreateView):
    model = models.CustomerProfile
    form_class = forms.CustomerForm
    template_name = 'invoice/form.html'
    success_url = '/home/'
    
class AddBusinessView(CreateView):
    models = models.BusinessProfile
    form_class = forms.BusinessForm
    template_name = 'invoice/form.html'
        
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect('invoice:home')
            
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class InvoiceCreateView(CreateView):
    model = models.Invoice
    form_class = forms.InvoiceForm
    template_name = 'invoice/invoice_form.html'
    
    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        context['items_formset'] = forms.InvoiceItemFormSet()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        items_formset = forms.InvoiceItemFormSet(self.request.POST)
        if form.is_valid() and items_formset.is_valid():
            return self.form_valid(form, items_formset)
        else:
            return self.form_invalid(form, items_formset)
    
    def form_valid(self, form, items_formset):
        self.object = form.save(commit=False)
        self.object.save()

        items_form = items_formset.save(commit=False)
        for items in items_form:
            items.invoice = self.object
            items.save()
        return redirect('invoice:invoice_list')
    
    def form_invalid(self, form,items_formset):
        return self.render_to_response(
            self.get_context_data(form=form,items_formset=items_formset)
        )
        
