# gemini_project

To setup project on any Linus, go through steps listed below :
Step 1 : Create virtual environment by running commang : # python -m venv <virtual-name>
Step 2 : Activating virtual Environment : # source <virtual-name>/bin/activate
Step 3 : cd into folder VendorFinder : # cd VendorFinder
Step 4 : install requirements for project using command : # pip install -r requirements.txt
Step 5 : make migrations for the database table using command : # python manage.py makemigrations services
Step 6 : Making tables into database using command : # python manage.py migrate
Step 7 : Create superuser using command : # python manage.py createsuperuser
Step 8 : Run server using command : python manage.py runserver
