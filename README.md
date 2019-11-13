# VendorFinder
## Description
> A platform to provide address and contact details of Vendoors of your locality to serve for the services you want. Find any kind of domestic or coorperative services like Plumbing, Electric Services, Carpenting, Cleaning, Pest Control etc.
## Documentation
Documentation of the project can be viewed in Docs folder.
## Technology Used
  * __FrontEnd__ : HTML, CSS, JavaScript, Bootstrap
  * __BackEnd__ : Python
  * __Framework__ : Django
  * __Database__ : We are using Django ORM, so you can use any Database you want. More can be found [here](https://docs.djangoproject.com/en/2.2/ref/databases/)
# Getting Started
## PreRequisite
Before you can use this project, you’ll need to go through some installations. minimal installation that’ll work can be found [here](https://docs.djangoproject.com/en/2.2/intro/install/)
## Project Setup
1. Create virtual environment in your project-folder by running command : ```python -m venv <virtual-env-name>  ```
2. Activate virtual environment by running command ```  source <virtual-env-name>/bin/activate```
3. cd into folder VendorFinder by running command : ```cd VendorFinder  ```
4. install requirements for project by running command :: ``` pip install -r requirements.txt ```  
5. Make migrations for the database table by running command : ```python manage.py makemigrations services  ```
6. Migrate tables to database by running command : ```python manage.py migrate  ```
6. Create superuser for admin access by running command : ```python manage.py createsuperuser  ```
7. Run server from terminal by running command : ``` python manage.py runserver '''
9. Go to your browser & type '127.0.0.1:8000' in the address bar to run project locally.
