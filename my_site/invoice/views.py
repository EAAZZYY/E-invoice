from django.shortcuts import render,redirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#imports used for htmltopdf
from django.template.loader import get_template
from xhtml2pdf import pisa

# Django CBV used
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from . import models

# Create your views here.
"""
Landing Page, Business, Customer and Invoice List View Logic Start
"""

def homeview(request):
    """Landing Page View"""
    return render(request, "invoice/home.html")

@login_required
def business_list(request):
    """ 
    Business list logic to list business registered by logged in user
    """
    businesses = models.BusinessProfile.objects.filter(user=request.user)
    return render(request, "invoice/business.html", context={"businesses":businesses})

@login_required
def customer_list(request):
    """ 
    Customer list logic
    returns list of customers registered to a business
    """
    business = models.BusinessProfile.objects.filter(user=request.user)
    customers = models.Customer.objects.filter(business__in=business)
    return render(request, "invoice/customer_list.html", context={"customers":customers})
    
    
class LoginRequired(LoginRequiredMixin):
    """
        LoginRequiredMixin
        Ensures only Logged in user can have access to CBV urls
    """
    login_url = '/accounts/login'
    redirect_field_name = 'next'
    
    def dispatch(self, request,*args, **kwargs):
        """
        Method to check if user is logged in else redirect to login
        """
        if not request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name()
                )
        return super(LoginRequired, self).dispatch(request,self,*args,**kwargs)

class InvoiceListView(LoginRequired, ListView):
    """
    Invoice List CBV
    Lists Invoices created under a business
    """
    model = models.Item
    template_name = 'invoice/invoice_list.html'
    
    def get_context_data(self, **kwargs):
        """
        Method to get extra context
        """
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        business_profile = models.BusinessProfile.objects.filter(user=self.request.user)
        invoices = models.Invoice.objects.filter(business_name__in = business_profile)
        context['invoices'] = invoices
        return context

"""
Landing Page, Business, Customer and Invoice List View Logic Ends
"""

"""
Business, Customer and Invoice Forms View Logic Start
"""

@login_required
def create_customer(request):
    """
    Logic to check if request method is Post
    """
    if request.method == "POST":
        form = forms.CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("invoice:customer_list")
        
    else:
        """Request method is Get """
        form = forms.CustomerForm()
    return render(request, "invoice/form.html", context={'form':form})

@login_required
def add_business(request):
    """
    Logic to check if request method is Post
    """
    if request.method == "POST":
        form = forms.BusinessForm(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect('invoice:business')
    else:
        """Request method is Get """
        form = forms.BusinessForm()
    return render(request, "invoice/form.html", context={"form":form})    


@login_required
def create_invoice(request):
    """
    Logic to display Invoice and Item form
    """
    if request.method == "POST":
        form = forms.InvoiceForm(request.POST)
        items_formset = forms.InvoiceItemFormSet(request.POST)
        if form.is_valid() and items_formset.is_valid():
            """logic to check if the form fields are filled correctly"""
            new_form = form.save(commit=False)
            new_form.save()
            item_formset = items_formset.save(commit=False)
            for item in item_formset:
                """ Logic to add invoice id to individual item row"""
                item.invoice = new_form
                item.save()
            return redirect("invoice:invoice_list")
    else:
        """Request method is Get """
        form = forms.InvoiceForm()
        items_formset = forms.InvoiceItemFormSet()
        context = {
            "form":form,
            "items_formset":items_formset
        }
    return render(request, "invoice/invoice_form.html", context)
"""
Business, Customer and Invoice Forms View Logic End
"""

@login_required
def invoice_detail(request, slug):
    """
    Logic to get invoice instance to display invoice detail
    """
    invoice = models.Invoice.objects.get(invoice_slug=slug)
    
    return render(request, 'invoice/invoice_detail.html', context={'invoice':invoice})

    
@login_required
def invoice_delete(request,slug):
    """
    Logic to get invoice instance to delete invoice
    """
    invoice = models.Invoice.objects.get(invoice_slug=slug)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice:invoice_list')    
    
    return render(request, 'invoice/delete.html', context={"invoice":invoice})
    
@login_required
def delete_customer(request, id):
    """
    Logic to get customer instance to delete customer
    """
    customer = models.CustomerProfile.objects.get(id=id)
    if request.method == 'POST':
        customer.delete()
        return redirect('invoice:business')
    return render(request, 'invoice/delete.html', context={'customer':customer})

@login_required
def delete_business(request, id):
    """
    Logic to get business instance to delete business
    """
    business = models.BusinessProfile.objects.get(id=id)
    if request.method == 'POST':
        business.delete()
        return redirect('invoice:business')
    return render(request, 'invoice/delete.html', context={'business':business})

@login_required
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
        
