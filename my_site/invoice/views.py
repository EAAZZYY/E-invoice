from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView,UpdateView
from django.views.generic.detail import DetailView
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from . import models
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

# Create your views here.

class LoginRequired(LoginRequiredMixin):
    login_url = '/accounts/login'
    redirect_field_name = 'next'
    
    def dispatch(self, request,*args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name())
        return super(LoginRequired, self).dispatch(request,self,*args,**kwargs)

class HomeView(TemplateView):
    template_name = 'invoice/home.html'

class BusinessListView(LoginRequired, ListView):
    model = models.CustomerProfile
    context_object_name = 'customers'
    template_name = 'invoice/business.html'
    
    def get_context_data(self, **kwargs):
        context = super(BusinessListView, self).get_context_data(**kwargs)
        business_profile = models.BusinessProfile.objects.filter(user=self.request.user)
        
        context['businesses'] = business_profile
        return context
    
class InvoiceListView(LoginRequired, ListView):
    model = models.Item
    template_name = 'invoice/invoice_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        business_profile = models.BusinessProfile.objects.filter(user=self.request.user)
        invoices = models.Invoice.objects.filter(business_name__in = business_profile)
        context['invoices'] = invoices
        return context

class CustomerCreateView(LoginRequired,CreateView):
    model = models.CustomerProfile
    form_class = forms.CustomerForm
    template_name = 'invoice/form.html'
    success_url = '/home/'
    
class AddBusinessView(LoginRequired,CreateView):
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
        return redirect('invoice:business')
            
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class InvoiceCreateView(LoginRequired,CreateView):
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
    

def pdf_convert(request, slug):
    template_path = 'invoice/pdf_convert.html'
    invoice=models.Invoice.objects.get(invoice_slug=slug)
    context = {'invoice':invoice }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="E-invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
        
@login_required
def invoicedetail(request, slug):
    invoice = models.Invoice.objects.get(invoice_slug=slug)
    # invoice_items = invoice.invoice_set.all()
    return render(request, 'invoice/invoice_detail.html', context={'invoice':invoice})

    
@login_required
def invoicedelete(request,slug):
    invoice = models.Invoice.objects.get(invoice_slug=slug)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice:invoice_list')    
    
    return render(request, 'invoice/delete.html', context={"invoice":invoice})
    
def deletecustomer(request, id):
    customer = models.CustomerProfile.objects.get(id=id)
    if request.method == 'POST':
        customer.delete()
        return redirect('invoice:business')
    return render(request, 'invoice/delete.html', context={'customer':customer})

def deletebusiness(request, id):
    business = models.BusinessProfile.objects.get(id=id)
    if request.method == 'POST':
        business.delete()
        return redirect('invoice:business')
    return render(request, 'invoice/delete.html', context={'business':business})
