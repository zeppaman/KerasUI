from django.db import models
from python_field.fields import PythonCodeField
from django import forms
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
#from django.core.urlresolvers import reverse

def path_file_name(instance, filename):
        path='data/datasets/'+str(instance.dataset.id)+'/'+ filename       
        return path

def path_model_name(instance, filename):
        path='data/models/'+str(instance.id)+'/'+ filename       
        return path
    

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
  




class DataSetItem(models.Model):
   
     label= models.CharField(max_length=200)
     #image
     image = models.ImageField(upload_to=path_file_name,max_length=300,db_column='imagePath')

     #relations
     dataset = models.ForeignKey(DataSet, on_delete=models.CASCADE)

   

     # def get_absolute_url(self):
     #    return reverse('management:item_edit', kwargs={'pk': self.pk})


