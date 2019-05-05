# usage
- run standalone.bat (this will install requirements apply `migrationd and run server)
- create the admin user using `python manage.py createsuperuser`
- navigate to http://127.0.0.1:8000/

install
python -m django --version 'check if django installed


#Api usage

```
POST http://127.0.0.1:8000/api/test/

Headers:
Content-Type:application/json
Authorization:Bearer <token>

Body
{
	"image":"<base 64 image",
	"dataset":1
}

```

The response

```
{
    "result": "<LABEL PREDICTED>"
}
```

# Tutorial

## Project setup
django-admin startproject kerasui ' create the project


`
kerasui/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py
`
These files are:

- The outer kerasui/ root directory is just a container for your project. The inner mysite/ directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. mysite.urls).
- manage.py: A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in jango-admin and manage.py.
- \_\_init\_\_.py: An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read more about packages in the official Python docs.
- mysite/settings.py: Settings/configuration for this Django project. Django settings will tell you all about how settings work.
- mysite/urls.py: The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in URL dispatcher.
- mysite/wsgi.py: An entry-point for WSGI-compatible web servers to serve your project. See How to deploy with WSGI for more details.



## run it
python manage.py runserver
or setup visual studio code to run django /
<image>

```py
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}\\kerasui\\manage.py",
            "args": [
                "runserver",
                "--noreload",
                "--nothreading"
            ],
            "django": true
        }
    ]
}
```


## settings configuration


```
```

## first run
make and apply migrations
```
python manage.py migrate
python manage.py createsuperuser
admin\admin2019!
```

## APP

## management
```
python manage.py startapp management

```

### Models
- DataSet
- DataItem

```
python manage.py makemigrations
```

## Oauth

client hUiSQJcR9ZrmWSecwh1gloi7pqGTOclss4GwIt1o
secret ZuuLK21sQ2uZxk8dVG7k6pO474FBlM6DEQs7FQvDh28gdLtbCDJwFFi0YlTlLsbz9ddjUa7Lun6ifYwkfwyGMD95WsCuzibFWIMpsZHMA039RIv1mOsYUO5nK5ZVv1hB


POST to http://127.0.0.1:8000/o/token/

```
POST /token HTTP/1.1
Host: http://127.0.0.1:8000/o/token/
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded
grant_type:password
username:admin
password:admin2019!
```
Response is
```
{
    "access_token": "h6WeZwYwqahFDqGDRr6mcToyAm3Eae",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "eg97atDWMfqC1lYKW81XCvltj0sism"
}
```

# Background worker

```
python manage.py startapp worker

```

# api

```
python manage.py startapp api

```



