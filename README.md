# Keras UI: Visual tool from image classification
KerasUI is a visual tool to allow easy training of model in image classification and allow to consume model as a service just calling API.

Main features:
- authenticated with oauth2
- allow full model customization
- you can upload yet trained model and consume via API
- test form and visual to check how the net works
- bulk upload of the training set


## usage
- run standalone.bat or sh standalone.bat (this will install requirements apply migrations and run the server, the same script works on UNIX and windows)
- create the admin user using `python manage.py createsuperuser`
- navigate to http://127.0.0.1:8000/

this requires python 3+, if you have multiple version installed please change the script according (i.e. pip3).

**How to manage dataset**

Keras UI allows uploading dataset items (image) into the web application. You can do it one by one or adding a zip file with many images in one shot. It manages multiple datasets so you can keep things separates.
After you have the images loaded, you can click the training button and run the training process.
This will train the model you have defined without any interaction from you. You will get back training result and if you are finicky you can go to the log file and see what the system output
![](https://github.com/zeppaman/KerasUI/blob/master/assets/keras-ui.dataset.gif?raw=true)

**How to test using web UI**

Tho avoid to lose sleep over, I provided a simple form where you can upload your image and get the result.

![](https://github.com/zeppaman/KerasUI/blob/master/assets/keras-ui.test-ui.gif?raw=true)

**How to use API UI or postman to test API**

All you have seen until now in the web UI can be replicated using API. 
![](https://github.com/zeppaman/KerasUI/blob/master/assets/keras-ui.api.gif?raw=true)



## API usage

This application use oauth2 to authenticate requests, so the first step you need is to get the token. This is a simple example for password flow. Please remember you have to enable the app (this is not created by default at first run). 

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


The API to get the prediction works in json post or form post. In json post the image is sent as base64 string. This double way to consume the service is useful because you may link it to a form or use with wget or curl tool directly as well you can use it from your application.

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
This project is part of the image classification context on Codeproject. Here a walkthrough on the technical part to explain how it is built and how it works.

The project stack:
- Python
- django framework
- keras, tensorflow,numpy
- sqlite (or other databases you like)

Tools used:
- Visual studio code
- Postman
- A web browser

### Project setup
The project is based on Django, so the first thing to do is to create a Django project using CLI. This requires to install Django from pip.

```
django-admin startproject kerasui ' create the project
```

This command will produce the following structure:
```
kerasui/
    manage.py
    kerasui/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```

These files are:

- *The outer kerasui/ root directory* is just a container for your project. The inner mysite/ directory is the actual Python package for your project. Its name is the Python package name you’ll need to use to import anything inside it (e.g. mysite.urls).
- *manage.py:* A command-line utility that lets you interact with this Django project in various ways. You can read all the details about manage.py in jango-admin and manage.py.
- *\_\_init\_\_.py:* An empty file that tells Python that this directory should be considered a Python package. If you’re a Python beginner, read more about packages in the official Python docs.
- *kerasui/settings.py:* Settings/configuration for this Django project. Django settings will tell you all about how settings work.
- *kerasui/urls.py:* The URL declarations for this Django project; a “table of contents” of your Django-powered site. You can read more about URLs in the URL dispatcher.
- *kerasui/wsgi.py:* An entry-point for WSGI-compatible web servers to serve your project. See How to deploy with WSGI for more details.



#### Run it
To check if all works, just run django with the built-in server (in production we will use wsgi interface to integrate with our favourite web server)
```
python manage.py runserver
```

You can also use  setup visual studio code to run django /

<image>

This is the django configuration:
```json
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


#### Settings configuration

Here the basic part of the configuration that tell:
- to use oauth 2 and session authentication so that: regular web user login and use the web site and rest sandbox, API user get the token and query the API services
- to use SQLite (you can change to move to any other DB)
- to add all Django modules (and our two custom: management UI and API)
- enable cors

```py

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

#### First run
Django uses a migration system that produces migration files from the model you defined. To apply migrations you just need to run the migrate command (makemigration to create migration files from model).

The user database start empty, so you need to create the admin user to login. This is done by the createsuperadmin command 

```
python manage.py migrate
python manage.py createsuperuser
admin\admin2019!
```

### How it's built
The app is separated into 3 modules:
- **Management part:** the web UI, the modules and all the core stuff
- **Background worker:** is a Django command that can be executed in background and is used to train models against the dataset
- **API:** this part exposes API to interact with application from outside. In example, this allows to add items to dataset from a third party application. *Moreover, the most common usage is to send an image and get the prediction result*

#### Management
To create an app on Django:

```
python manage.py startapp management

```
This will create the main files for you. In this module the most we use is about Model and Model representation:
- *module.py:* here are all models with field specifications. By such class definition, all is set to have a working CRUD over entities
- *admin.py*: this layer describes how to show and edit data with forms.

**The data model**
Our data model is very simple. Assuming that we want to train only one model per dataset (this may be a limit if you would reuse dataset with multiple models...), we have
- *DataSet*: this contains the model, the model settings, and the name of the dataset.
- *DataSetItem*: this contains the dataset items, so one image per row with the label attached.


Here just a sample of models and model representation:

```py
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

Django works in code-first approach, so we will need to run `python manage.py makemigrations` to generate migration files that will be applied to the database.



```
python manage.py makemigrations
```


#### Background worker
To create the background worker we need a module to host it, and I used the management module.
Inside it, we need to create a `management` folder (sorry for the name that is the same as the main module, I hope this is not a threat).
Each file on it can be run via `python manage.py commandname` or via API.

In our case, we start the command in a background process via regular Django action

This is the relevant part:

```py

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

#### API
The API is created in a separated app

```
python manage.py startapp API

```

Basically all CRUD model can be exposed by API, however, you need to specify how to serialize it

```py

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

```py
class DataSetItemViewSet(viewsets.ModelViewSet):
   
    queryset = DataSetItem.objects.all()
    serializer_class = DataSetItemSerializer

class DataSetViewSet(viewsets.ModelViewSet):
   
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
```

Finally, you need to define all routes and map viwset to url. This will be enough to consume model as api
```py
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

### The training

The algorithm is very easy:
1. Take all images from the dataset 
2. Normalize them and add to a labeled list
3. Create the model how it is specified into the dataset model
4. train it

This is the piece of code that query dataset items and load images:

```py
def load_data(self, datasetid):
        self.stdout.write("loading images")
        train_data = []
        
        images = DataSetItem.objects.filter(dataset=datasetid)
        labels = [x['label'] for x in  DataSetItem.objects.values('label').distinct()]
      
        for image in images:
            self.stdout.write("Loading {0}".format(image.image))
            image_path = image.image.path
            if "DS_Store" not in image_path:           
                index=[x for x in range(len(labels)) if labels[x]==image.label]
                label = to_categorical([index,],len(labels))
                
                img = Image.open(image_path)
                img = img.convert('L')
                img = img.resize((self.IMAGE_SIZE, self.IMAGE_SIZE), Image.ANTIALIAS)
                train_data.append([np.array(img), np.array(label[0])])
            
        return train_data
```

Take a look at:
```py
labels = [x['label'] for x in  DataSetItem.objects.values('label').distinct()]
label = to_categorical([index,],len(labels))
```

this assigns an order to all the labels, i.e. `["CAT","DOGS"]` then `to_categorical` convert the positional index to the one-hot representation. To tell in simpler words, this make CAT =[1,0] and DOG=[0,1]


To train the model
```py
   model=Sequential()
   exec(dataset.process)
   model.add(Dense(len(labels), activation = 'softmax'))
   model.fit(training_images, training_labels, batch_size=dataset.batchSize, epochs=dataset.epochs, verbose=dataset.verbose)
```

Note that the dataset.process is the python model definition you entered into web admin and you can tune as much you want. The last layer is added outside the user callback to be sure to match the array size.

The fit method just runs the train using all data (keras automatically make a heuristic separation of test and training set, for now, it's enough, in future we can plan to let the user choose percentages of data to use in each part or mark items one by one).

Finally we store the trained model:

```py
datasetToSave=DataSet.objects.get(pk=datasetid)
datasetToSave.progress=100
datasetToSave.model_labels=json.dumps(labels)
temp_file_name=str(uuid.uuid4())+'.h5'
model.save(temp_file_name)
datasetToSave.model.save('weights.h5',File(open(temp_file_name, mode='rb')))
os.remove(temp_file_name)
datasetToSave.save()
```
Note that I save also the label order beacuse must be the same of the model to match the one-hot convention.


### the prediction

There is a common method that, given the sample and the dataset, retrieve the model, load it and make the prediction.
This is the piece of code:


```py
def predict(image_path,datasetid):
        
            dataset=DataSet.objects.get(pk=datasetid)
            modelpath=dataset.model.path
            model=load_model(modelpath)
            labels=json.loads(dataset.model_labels)
            
            img = Image.open(image_path)
            img = img.convert('L')
            img = img.resize((256, 256), Image.ANTIALIAS)

            result= model.predict(np.array(img).reshape(-1,256,256, 1))
            max=result[0]
            idx=0
            for i in range(1,len(result)):
                if max<result[i]:
                    max=result[i]
                    idx=i


            return labels[idx]
```
The model is loaded using `load_model(modelpath)` and the labels are from the database. The model prediction output as a list of values, it is chosen the higher index and used to retrieve the correct label assigned to the network output at the training time.



# Acknowledgements
This article is part of the image classification challenge. Thanks to the article [Cat or not](https://www.codeproject.com/Articles/4023566/Cat-or-Not-An-Image-Classifier-using-Python-and-Ke) of Ryan Peden where I find the basics to manage the training process and images to test the tool.


