# Askcenter
Askcenter is basically a web application where users can post their questions on the different topics and also can reply to those posted questions.

Steps to run the project
Clone the repository
Create python3.8 virtual environment and activate it
Go to the project root directory where manage.py file is present
Install the dependencies by using pip3 install requirements.txt
In the project directory where manage.py file is present create a file with name .environ_var for saving the SECRET Key here
and inside that file add below line-
 SECRET_KEY="your-key" 
 Replace your-key with your SECRET KEY
 Now run the command - python3 manage.py makemigrations
 And also - python3 manage.py migrate
 Then create superuser by this command - python3 manage.py createsuperuser
 Now run this - python3 manage.py runserver

