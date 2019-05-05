KerasUI is a visual tool to allow easy traing of model in image classification and allow to consume model as a service just calling api.

Main features:
- authenticated with oauth2
- allow full model customization
- you can upload yet trained model and consume via api
- test form and visual to check how the net works
- bulk upload of training set


## usage
- run standalone.bat (this will install requirements apply migrations and run server)
- create the admin user using `python manage.py createsuperuser`
- navigate to http://127.0.0.1:8000/

** how to manage dataset **
![](https://github.com/zeppaman/KerasUI/blob/master/assets/keras-ui.dataset.gif?raw=true)
** how to test using web UI **
![](https://github.com/zeppaman/KerasUI/blob/master/assets/keras-ui.test-ui.gif?raw=true)
** how to use api UI or postman to test api **
![](https://github.com/zeppaman/KerasUI/blob/master/assets/keras-ui.api.gif?raw=true)



## Api usage

To get the token:

```
Assuming
client hUiSQJcR9ZrmWSecwh1gloi7pqGTOclss4GwIt1o
secret ZuuLK21sQ2uZxk8dVG7k6pO474FBlM6DEQs7FQvDh28gdLtbCDJwFFi0YlTlLsbz9ddjUa7Lun6ifYwkfwyGMD95WsCuzibFWIMpsZHMA039RIv1mOsYUO5nK5ZVv1hB

POST to http://127.0.0.1:8000/o/token/

Headers:
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded

Body:
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


The api to get the prediction works in json post or form post. In json post the image is sent as base64 string.

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
for a full api documentation you can refer to the [postman file](https://github.com/zeppaman/KerasUI/blob/master/assets/kerasui.postman_collection.json)

## Tutorial
This project is part of the image classification context on codeproject. Here a walkthorugt.

### Project setup
The poject is based on django, so first things to to is to create a django project using cli.

```
django-admin startproject kerasui ' create the project
```

This will prduce the following structure:
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



#### run it
To check if all works, just run django with the built-in server (in production we will use wsgi interface to integrate with our favourite web server)
```
python manage.py runserver
```

You can also use  setup visual studio code to run django /

<image>

This is the django configuration:
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


#### settings configuration

Here the basic part of configuration that tell:
- to use oauth 2 and session authentication so that: regular web user login and use the web site and rest sandbox, api user get the token and query the api services
- to use sqlite (you can chance to move to any other db)
- to add all djagno modules (and our two custom: management UI and api)
- enable cors

```

INSTALLED_APPS = [
    'python_field',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'corsheaders',
    'rest_framework',  
    'management',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
   # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'kerasui.urls'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
  
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

#### first run
make and apply migrations
```
python manage.py migrate
python manage.py createsuperuser
admin\admin2019!
```

### APP
The app is separated in 3 modules:
- **Management part:** the web UI, the modules and all the core stuff
- **Background worker:** is a django command that can be executed in background and is used to train models against dataset
- **API:** this part expose api to interact with application from outside. In example, this allow to add item to dataset from a third party application. *Moreover, the most common usage is to send an image and get the prediction result*

## management
To create an app on django:

```
python manage.py startapp management

```
This will create the main files for you. In this module the most we use is about Model and Model representation:
- *module.py:* here are all models with field specification. By such class definition all is set to have a working CRUD over entities
- *admin.py*: this layer describe how to show and edit data with forms.

**The data model**
Our data model is vey simple. Assuming that we want to train only one model per dataser (this may be a limit if you would reuse dataset with multiple models...), we have
- *DataSet*: this contains the model, the model settings, and the name of the dataset.
- *DataSetItem*: this contains the dataset items, so one image per row with the label attacched.


Here just a sample 
```
#from admin.py
class DataSetForm( forms.ModelForm ): 


    process =forms.CharField( widget=forms.Textarea(attrs={'rows':40, 'cols':115}), initial=settings.PROCESS_TEMPLATE )
    model_labels =forms.CharField(initial="[]")
    class Meta:
        model = DataSet
        fields = ['name', 'process','epochs','batchSize','verbose','model_labels','model']
        widgets = {
          'process': forms.Textarea(attrs={'rows':20, 'cols':200}),
          }
    
def train(modeladmin, request, queryset):
       for dataset in queryset:
        DataSetAdmin.train_async(dataset.id)

class DataSetAdmin(admin.ModelAdmin):
    list_display = ('name','epochs','batchSize','verbose','progress')
    inlines = [
      #  DataSetItemInline,
    ]
    form=DataSetForm
    actions = [train]
    change_list_template = "dataset_changelist.html"


    @staticmethod
    def train(datasetid):
        call_command('train',datasetid)
    @staticmethod
    def train_async(datasetid):
        t = threading.Thread(target=DataSetAdmin.train, args=(datasetid,))
        t.setDaemon(True)
        t.start()


admin.site.register(DataSet,DataSetAdmin)

#from model.py

class DataSet(models.Model):
    name= models.CharField(max_length=200)
    process = models.CharField(max_length=5000, default=settings.PROCESS_TEMPLATE)
    model = models.ImageField(upload_to=path_model_name,max_length=300,db_column='modelPath',blank=True, null=True)
    #weights = models.ImageField(upload_to=path_model_name,max_length=300,db_column='weightPath',blank=True, null=True)
    batchSize = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)],default=10)
    epochs = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)],default=10)
    verbose = models.BooleanField(default=True)
    progress = models.FloatField(default=0)    
    model_labels= models.CharField(max_length=200)
    def __str__(self):
        return self.name
	
```

Django works in code-first approach, so we will need to run `python manage.py makemigrations` to generate migration files that will be applied to database.



```
python manage.py makemigrations
```


# Background worker
To create the background worker we need a module to host it, and I used the management module.
Inside it we need to create a `management` folder (sorry for name that is the same of the main module, I hope this is not a treath).
Each file on it can be run via `python manage.py commandname` or via api.

In our case we start the command in a background process via regular django action

This is the relevant part:

```

class DataSetAdmin(admin.ModelAdmin):
   
    actions = [train]


    # ....
    
    @staticmethod
    def train(datasetid):
        call_command('train',datasetid)
    @staticmethod
    def train_async(datasetid):
        t = threading.Thread(target=DataSetAdmin.train, args=(datasetid,))
        t.setDaemon(True)
        t.start()
```

# api
The api is created in a separated app

```
python manage.py startapp api

```

Basically all CRUD model can be exposed by api, however you need to specify how to serialize it

```

class DataSetItemSerializer(serializers.HyperlinkedModelSerializer):
    image = Base64ImageField()
    dataset=   serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = DataSetItem

        # Fields to expose via API
        fields = ('label', 'image', 'dataset')


class DataSetSerializer(serializers.HyperlinkedModelSerializer):  
   
    class Meta:
        model = DataSet
        fields = ('name', 'process')
```

You need also to create ViewSet (mapping between the model and the data presentation:

```
class DataSetItemViewSet(viewsets.ModelViewSet):
   
    queryset = DataSetItem.objects.all()
    serializer_class = DataSetItemSerializer

class DataSetViewSet(viewsets.ModelViewSet):
   
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
```

Finally, you need to define all routes and map viwset to url. This will be enough to consume model as api
```
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'datasetitem', views.DataSetItemViewSet)
router.register(r'dataset', views.DataSetViewSet)
router.register(r'test', views.TestItemViewSet, basename='test')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += staticfiles_urlpatterns()

```




