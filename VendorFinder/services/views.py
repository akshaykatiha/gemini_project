from django.shortcuts import (
    render, redirect
)
from .models import (
    User, Vendor, Customer, Service, SubService, VendorService, Invoice
)
from .forms import (
    VendorForm, CustomerForm, UpdateProfile, VendorServiceForm
)
from django.contrib.auth import (
    authenticate, update_session_auth_hash, login
)
from django.db.models import Q,F
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator
from django.db import connection, transaction
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    user_type = ''
    if request.user.is_authenticated:
        user_type = request.user.is_vendor 
    context = {
        'user_type' : user_type,
    }
    template_name = 'services/index.html'
    return render(request, template_name=template_name, context=context)


##################  TO REDIRECT VENDOR TO IT'S SERVICE PROVIDED PAGE ###############
@login_required
def service_provided(request):
    if request.user.is_authenticated:
        user_type = request.user.is_vendor
        user_id = request.user.id
        username = request.user.username
        if user_type:
            vendor_detail = VendorService.objects.select_related('service','sub_service','vendor','user').filter(vendor_id=user_id,is_active=True)
            context = {
            'vendor_detail' : vendor_detail,
            'username' : username,
            }
            template_name = 'services/vendorprofile.html'
            return render(request, template_name=template_name, context=context)
        else :
            messages.warning(request, 'You are not authorised to view this page.')
            return redirect('index')
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        
    
################# VIEW TO TAKE RQUEST FROM NEW USER FOR SIGNUP############
def signup(request):
    if request.user.is_authenticated:
            return HttpResponse("You are already signed in")
    else :
        template_name = 'registration/multiuser_signup.html'
        return render(request, template_name=template_name)


################# VIEW TO TAKE RQUEST FROM NEW USER FOR SIGNUP############
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if request.user.is_vendor:
            return render(request, 'services/vendorprofile.html')
        else:
            return render(request, 'services/services.html')
    else:
        return redirect('login')

################# VIEW TO SIGNUP A NEW USER AS VENDOR ############
def vendor_signup(request):
    if request.user.is_authenticated:
            return HttpResponse("You are already signed in")
    else :
        if request.method == 'POST':
            form = VendorForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                authenticate(username=username, password=raw_password)
                messages.success(request, 'Successfully Signed as Vendor. Please Login to continue')
                #login(request, user)
                return redirect('login')
        else:
            context = {
            'form' : VendorForm(),
            'user_type' : 'Vendor'
            }
        return render(request, 'registration/signup.html', context)


################# VIEW TO SIGNUP A NEW USER AS CUSTOMER ############
def customer_signup(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            authenticate(username=username, password=raw_password)
            messages.success(request, 'Successfully Signed as Customer. Please Login to continue')
            #login(request, user)
            return redirect('login')
    else:
        form = VendorForm()
    return render(request, 'registration/signup.html', {'form': form})


################# TO VIEW PROFILE OF A REGISTERED USER ############
@login_required
def view_profile(request):
    # If user is not authenticated, send him/her to login page
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return render (request,'registration/view_profile.html')


################# VIEW TO UPDATE PROFILE OF A REGISTERED USER ############
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=request.user)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.save()
            messages.success(request, 'Your profile was updated successfully !')
            return redirect('view_profile')
            
        else:
            messages.error(request, 'Please fill details correctly.')
            return redirect('update_profile')
    else:
        form = UpdateProfile(instance=request.user)
        return render (request,'registration/update_profile.html',{'form': form})
        

################# VIEW TO UPDATE PROFILE OF A REGISTERED VENDOR ############
@login_required
def add_service(request, username):
    if request.user.is_authenticated:
        username = request.user.username
    if request.method == 'POST':
        form = VendorServiceForm(request.POST)
        if form.is_valid():
            # form = VendorServiceForm()
            # form = VendorServiceForm(initial={'user' : username, 'vendor' : username})
            form.save()
            messages.success(request, 'A new SubService was added to your profile')
            #login(request, user)
            return redirect('view_profile')
    else:
        form = VendorServiceForm()
    return render(request, 'registration/vendorprofile.html', {'form': form})


################# VIEW TO UPDATE PROFILE OF A REGISTERED VENDOR ############
@login_required
def update_service(request):
    return render(request, 'registration/vendorprofile.html', {'form': form})

################# VIEW TO CHANGE PASSWORD OF A REGISTERED USER ############
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')

            # Sending Confirmation Mail on successful update of password
            if request.user.is_authenticated:
                username = request.user.username
                name = request.user.first_name
                email = request.user.email
                # time = request.user.row_update_date
            subject = 'Password Changed Successfully'
            if name is '':
                name = username
            message = ' Hi '+name+'\n Your Password has been changed Successfully.\n' #+ time
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list, fail_silently=False)
            return redirect('view_profile')
        else:
            messages.error(request, 'Please enter password correctly.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


################# VIEW TO SEE ALL THE SERVICES PROVIDED TO CUSTOMERS ############
def services(request):
    service = Service.objects.all()
    paginator = Paginator(service, 6)
    page = request.GET.get('page')
    service_list = paginator.get_page(page)
    count = paginator.get_page(page)
    context = {
        'service_list' : service_list,
        'count' : count,
    }
    return render (request, 'services/services.html', context)


################# VIEW TO SEE ALL THE SUBSERVICES RELATED TO A SERVICE ############
def service_info(request, id, service_name):
    service_name = service_name
    # subservice = SubService.objects.filter(service=id).select_related()
    subservice = SubService.objects.select_related('service').filter(service_id=id)
    #total_subservice = SubService.objects.filter(service=id).select_related().count()
    paginator = Paginator(subservice, 6)
    page = request.GET.get('page')
    subservice_list = paginator.get_page(page)
    count = paginator.get_page(page)
    context = {

        'subservice_list' : subservice_list,
        'service_name' : service_name,
        'count' : count,
        #'total_subservice' : total_subservice,
    }
    return render(request, 'services/subservice.html', context)


################# VIEW TO DISPLAY ALL THE VENDORS RELATED TO SUBSERVICES ############
def vendors(request, service_id, service_name, id, sub_service_name):
    # cursor = connection.cursor()
    # cursor.execute("SELECT first_name, last_name, email, phone, service_name, sub_service_name, sub_service_charge from vendor_service join sub_service on vendor_service.sub_service_id = sub_service.id join service on sub_service.service_id = service.id join vendor on vendor_service.vendor_id = vendor.vendor_id join user on vendor.vendor_id = user.id where service_name = 'Electrician'")
    # row = cursor.fetchone()
    # sub_service_name = sub_service_name
    #total_subservice = SubService.objects.filter(service=id).select_related().count()
    sub_service_name = sub_service_name
    vendors = VendorService.objects.select_related('service','sub_service','vendor','user').filter(service_id=service_id,sub_service_id=id).order_by('sub_service_charge')
    paginator = Paginator(vendors, 6)
    page = request.GET.get('page')
    vendor_detail = paginator.get_page(page)
    count = paginator.get_page(page)
    context = {
        'vendor_detail' : vendor_detail,
        'sub_service_name' : sub_service_name,
        #'sub_service' : sub_service,
        'count' : count,
        # 'vendor_info' : vendor_info,
        #'total_subservice' : total_subservice,
    }
    return render(request, 'services/vendorservice.html', context)


################# VIEW TO DISPLAY COMPLETE INFO OF VENDOR IN DETAIL ############
@login_required
# At this point, we need our customer to authenticate because here we have to display 
# personal information like email and phone number of our vendors

def vendor_detail(request):
    return render (request,'services/vendor-profie.html')


################# VIEW TO SEND SERVICE REQUEST MAIL ############
@login_required
# At this point, we need our customer to authenticate because here we have to display 
# personal information like email and phone number of our vendors

def service_request(request):
    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')


################# VIEW TO VIEW THE CHECKOUT PAGE ############
@login_required
def booking_details(request, id, vendor_id, service_id, sub_service_id):
    vendor = User.objects.values('first_name','last_name','email','phone','image').filter(id=vendor_id)
    service_charge = Service.objects.all().filter(id=service_id)
    for i in service_charge:
        service_charge = i.service_charge
    sub_service_charge = VendorService.objects.all().filter(id=id)
    for i in sub_service_charge:
        sub_service_charge = i.sub_service_charge
    total = service_charge + sub_service_charge
    tax = 0.12 * float(total)
    total = float(total) + tax

    customer_id = request.user.id
    print(id)
    # q = Invoice.objects.create(vendor=vendor_id,customer=customer_id,service=service_id,sub_service=sub_service_id,total=total)
    
    context = {
        'vendor' : vendor,
        'service_charge' : service_charge,
        'sub_service_charge' : sub_service_charge,
        'vendor_id' : vendor_id,
        'total' : total,
        'tax' : tax,
    }
    return render (request, 'services/booking.html', context)

################# VIEW TO BOOK THE VENDOR ############
@login_required
def confirm_booking(request, vendor_id):
    user_username = request.user.username
    user_name = request.user.first_name
    user_email = request.user.email
    user_phone = request.user.email
    user_address = request.user.email

    vendor = User.objects.all().filter(id=vendor_id)
    for i in vendor:
        vendor_username = i.username
        vendor_name = i.first_name
        vendor_phone = i.phone
        vendor_email = i.email

    # Sending confirmation  mail to USER
    subject = 'Congratulations ! Your Booking is confirmed.'
    if user_name is '':
        user_name = user_username
    message = ' Hi '+user_name+'\n Your Booking has been confirmed successfully.Please find the details of your booking below :\n Name :'+ vendor_name +'\n Phone :' +vendor_phone+ '\n Email :' +vendor_email+ '\n ' #+ time
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail( subject, message, email_from, recipient_list, fail_silently=False)

    # # Sending confirmation  mail to USER
    subject = 'Request for Booking received.'
    if vendor_name is '':
        vendor_name = vendor_username
    message = ' Hi '+vendor_name+'\n Booking with following details has been received. Please find the details of your customer below :\n Name :'+ user_name +'\n Phone :' +user_phone+ '\n Email :' +user_email+ '\n Address :' + user_address 
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [vendor_email]
    send_mail( subject, message, email_from, recipient_list, fail_silently=False)
    
    messages.success(request, 'Congratulations !Your Booking has been confirmed')
    return render (request, 'services/ordersummary.html')


################# VIEW TO SEND MAIL  ############
@login_required
def order_summary(request):
    subject = 'New Service Request'
    message = ' Hi, I was looking for a new service from your site. Can you please provide it ?'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['akshaykatiha@gmail.com','akshay.katiha@geminisloutions.in',]
    send_mail( subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('redirect to a new page')