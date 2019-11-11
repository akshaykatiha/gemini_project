from django.urls import path, re_path
from services import views as ser_views

urlpatterns = [
    path('', ser_views.index, name= 'index'),

    #URLs for signup
    path('signup/',ser_views.signup, name='signup'),
    path('vendor_signup/',ser_views.vendor_signup, name='vendor_signup'),
    path('customer_signup/',ser_views.customer_signup, name='customer_signup'),
    # path('user-login/',ser_views.login_view, name='user_login'),
    
    #URLs for profile
    path('view_profile/',ser_views.view_profile, name='view_profile'),
    path('vendor-profile/',ser_views.service_provided, name='vendor_profile'),
    path('service-request/',ser_views.service_request, name='service_request'),
    path('update_profile/',ser_views.update_profile, name='update_profile'),
    path('vendor-profile/<str:username>/',ser_views.add_service, name='add_service'),
    path('update-service/',ser_views.update_service, name='update_service'),
    re_path(r'^password/$', ser_views.change_password, name='change_password'),

    #URLs for queries
    path('services/',ser_views.services, name='services'),
    re_path(r'^services/(?P<id>\d+)/(?P<service_name>[\w ]+)/$', ser_views.service_info, name='services'),
    path('services/<int:service_id>/<str:service_name>/<int:id>/<str:sub_service_name>/', ser_views.vendors, name='services'),
    # path('confirm-booking/',ser_views.confirm_booking, name='confirm-booking'),
    path('confirm-booking/<int:id>/<int:vendor_id>/<int:service_id>/<int:sub_service_id>/', ser_views.booking_details, name='confirm-booking'),
    path('confirm-booking/<int:vendor_id>/', ser_views.confirm_booking, name='confirm_booking'),
    path('order-summary/<int:id>/<int:vendor_id>/<int:service_id>/', ser_views.booking_details, name='confirm-booking'),

    

    

]
