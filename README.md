# Chat_test
# Overview
Django chat

# Requirements

    Python 3.6.7
    Django 2.1
    psycopg2 2.7.3.1
    crispy-forms 1.7.2
    postgresql


# Install
```
$ git clone https://github.com/KidProger/Chat_test
```

# Usage

Example:
```
$ cd Chat_test
$ create your virtual environment
$ pip install -r requirements.txt  
$ cd test_project
  change settings.py for your user and database or create your databse and user as in example:
        'NAME': 'chat_db',
        'USER' : 'kolyaadmin',
        'PASSWORD' : 'katyara123'
$ cd Chat_test
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver

open the website and input
http://127.0.0.1:8000/
```
# URLS
```
http://127.0.0.1:8000/ - homepage
http://127.0.0.1:8000/signup/ - registration
http://127.0.0.1:8000/users/login/ - login
http://127.0.0.1:8000/chat/ - List of available chats for current user
