# Import
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser #BaseUserManager
from django.core.validators import (
    RegexValidator,
    MaxValueValidator,
    MinValueValidator
)


# CHOICE_FIELDS
GENDER_CHOICE = [
        ('F','Female'),
        ('M','Male'),
        ('N','Not to Say'),
]

STATUS_CHOICE = [
        ('R','Requested'),
        ('A','Approved'),
        ('C','Complete'),
        ('E','Ended'),
]
# Models Here
# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None):
#         if not username:
#             raise ValueError('Enter a Valid username')

#         user = self.model(
#             username = username
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password):
#         user = self.create_user(
#             username,
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    phone = models.CharField(validators=[RegexValidator(regex=r'^[9876]\d{9}$', message="Enter 10 digit mobile number without any prefix(+91 or 0)", code='nomatch'
    )],
    max_length=10,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True)
    pincode = models.CharField(max_length=6,blank=True) 
    address = models.CharField(max_length=124,blank=True)
    city = models.CharField(max_length=124,blank=True)
    state = models.CharField(max_length=124,blank=True)
    image = models.ImageField(upload_to='static/media',blank=True,null=True)
    #row_insert_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_insert_date = models.DateTimeField(auto_now_add=True)
    #row_update_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_update_date = models.DateTimeField(auto_now=True)

    #objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name_plural = 'user'


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     customer_served = models.PositiveSmallIntegerField()
#     service_taken = models.PositiveSmallIntegerField()
#     rating = models.PositiveSmallIntegerField()
#     #row_insert_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     #row_insert_date = models.DateTimeField(auto_now_add=True)
#     #row_update_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     #row_update_date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#             return self.user.username
#     class Meta:
#         db_table = 'profile'

    
class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    customer_served = models.PositiveSmallIntegerField()
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    #vendor_image = models.ImageField(upload_to='static/media',blank=True,null=True)
    #number_of_services = models.PositiveSmallIntegerField() #Used to track total number of services served by a vendor
    #active_since = models.DateField()

    def __str__(self):
       return self.user.username
    class Meta:
        db_table = 'vendor'
        verbose_name_plural = 'vendor'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    service_taken = models.PositiveSmallIntegerField()
    #customer_image = models.ImageField(upload_to='static/media',blank=True,null=True)
    #active_since = models.DateField()  
      
    def __str__(self):
       return self.user.username
    class Meta:
        db_table = 'customer'
        verbose_name_plural = 'customer'

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    #admin_image = models.ImageField(upload_to='static/media',blank=True,null=True)
    #qualification = model.TextField()
    #member_since = model.DateTime(auto_now=True)

    def __str__(self):
       return self.user.username
    class Meta:
        db_table = 'admin'
        verbose_name_plural = 'admin'


class Otp(models.Model):
    otp_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    generation_time = models.DateTimeField(auto_now=True)
    #expiry_time = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #    return self.user.username

    class Meta:
        db_table = 'otp'
        verbose_name_plural = 'otp'


class Status(models.Model):
    is_active = models.BooleanField(default=True)
    status_name = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True)
    # description = models.TextField()
    #row_insert_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_insert_date = models.DateTimeField(auto_now_add=True)
    # row_update_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # row_update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
            return self.status_name
    class Meta:
        #abstract = True
        #If in future, we are not interested to create table for Status
        #we can set abstract = True
        db_table = 'status'
        verbose_name_plural = 'status'


class Service(models.Model):
    is_active = models.BooleanField(default=True)
    service_name = models.CharField(max_length=124)
    service_charge = models.DecimalField(max_digits=5, decimal_places=2)
    service_image = models.ImageField(upload_to='static/media',blank=True,null=True)
    service_description = models.CharField(max_length=124,blank=True)
    
    #To keep track of admin, who has added the service
    #row_insert_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_insert_date = models.DateTimeField(auto_now_add=True)
    #row_update_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
       return self.service_name

    class Meta:
        db_table = 'service'
        verbose_name_plural = 'service'


class SubService(models.Model):
    is_active = models.BooleanField(default=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    sub_service_name = models.CharField(max_length=124)
    #sub_service_image = models.ImageField(upload_to='static/media',blank=True,null=True)
    
    #To keep track of admin, who has added the service
    #row_insert_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_insert_date = models.DateTimeField(auto_now_add=True)

    #To keep track of admin, who has added the service
    #row_update_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sub_service_name

    class Meta:
        db_table = 'sub_service'
        verbose_name_plural = 'sub service'


class VendorService(models.Model):
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE)
    sub_service_charge = models.DecimalField(max_digits=5, decimal_places=2)
    #row_insert_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_insert_date = models.DateTimeField(auto_now_add=True)
    #row_update_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
       return self.vendor.user.username+" "+self.sub_service.sub_service_name

    class Meta:
        db_table = 'vendor_service'
        verbose_name_plural = 'vendor service'

class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    sub_service = models.ForeignKey(SubService, on_delete=models.CASCADE)
    status = models.ForeignKey(Status,on_delete=models.SET_NULL, null=True)
    total_charge = models.DecimalField(max_digits=6, decimal_places=2)
    # description = models.TextField()
    #row_insert_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_insert_date = models.DateTimeField(auto_now_add=True)
    #row_update_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    row_update_date = models.DateTimeField(auto_now=True)

    #def __str__(self):
    #    return self.service.service_name
    # What should be returned?

    class Meta:
        db_table = 'invoice'
        verbose_name_plural = 'invoice'