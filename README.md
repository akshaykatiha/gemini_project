# VendorFinder
## Description
> A platform to provide address and contact details of Vendors of your locality to serve for the services you want. Find any kind of domestic or coorperative services like Plumbing, Electric Services, Carpenting, Cleaning, Pest Control etc.
## Documentation
Documentation of the project can be viewed in Docs folder.
## Technology Used
  * __FrontEnd__ : HTML, CSS, JavaScript, Bootstrap
  * __BackEnd__ : Python
  * __Framework__ : Django
  * __Database__ : We are using Django ORM, so you can use any Database you want. More can be found [here](https://docs.djangoproject.com/en/2.2/ref/databases/)
# Getting Started
## Pre-Requisites
Before you can use this project, you’ll need to install __Python__, __Django__ and __Database__. Minimal installation that’ll work can be found [here](https://docs.djangoproject.com/en/2.2/intro/install/)
## Project Setup
* Create and activate a virtual environment in your project-folder 
```bash 
$python -m venv <virtual-env-name>
$source <virtual-env-name>/bin/activate
```

* In your project root, install specific project requirements  
``` bash
$cd VendorFinder
$pip install -r requirements.txt 
```  
* Make migrations for the database table  
``` bash
$python manage.py makemigrations services 
```
* Migrate tables to database 
``` bash
$python manage.py migrate 
```
* Create superuser for admin access  
``` bash
$python manage.py createsuperuser
```
* Run server from terminal 
``` bash
$python manage.py runserver
```
* Go to your browser & type __127.0.0.1:8000/services__ in the address bar to run project locally.
