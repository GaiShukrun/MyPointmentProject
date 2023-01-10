# MyPointmentProject
Welcome to our SCE project

![developers](https://img.shields.io/badge/Developed%20By%3A-Furman%20Vlad,%20Shukrum%20Gai,%20Berko%20Tal,%20Hazan%20Ori-red)

## HOW TO RUN THIS PROJECT
- Download Project Zip Folder and Extract it
- Move to project folder in Terminal. Then run following commands :
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
- Now enter following URL in your browser installed on your PC
```
http://127.0.0.1:8000/
```
For admin account, please create one with superuser! (if you don't know how, [click here](https://www.geeksforgeeks.org/how-to-create-superuser-in-django/)).

## Drawbacks/LoopHoles
- Before even starting using the system, the admin needs to create the 4 doctors manually from the [admin panel](http://127.0.0.1:8000/admin/auth/user/add/), the doctor's specialty is their username, so create 4 accounts with the following usernames (first letter is capitalized): Cardiologist, Oncologist, Psychiatrist, Neurologist.
- Change doctors usernames is forbidden.
- As a doctor make sure your inputs in 'TimeTaken' is >= 0 ('TimeTaken' default is None, 0 is "Not Appeared" and any other positive number it's the time taken of the appointment (in minutes)).

