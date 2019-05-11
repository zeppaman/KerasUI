from django.contrib import admin
from management.models import DataSet,DataSetItem
from django import forms
from django.db import models
from django.conf import settings
from django.core.management import call_command
import threading
from django.core.files.storage import FileSystemStorage
import zipfile
import os
from os import listdir
from os.path import isfile, join
import shutil
from django.core.files import File
from django.urls import path
from django.core.files import File
from django.contrib import messages
from management.kmanager import KManager
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy
import logger

logger = logging.getLogger(__name__)

class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('KerasUI')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('KerasUI')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('KerasUI')

admin_site = MyAdminSite()

admin.site.site_header = 'Keras UI'


def upload_file_name(instance, filename):
        path='tmp/'+str(instance.dataset.id)+'/'+ filename       
        return path


class TestForm(forms.Form):
    IMAGE_SIZE=256
    #image
    image = forms.ImageField()
    dataset = forms.ModelChoiceField(queryset= DataSet.objects.all())

    def process(self,request):
        image = self.cleaned_data['image']
        dataset = self.cleaned_data['dataset']
        image_path=image.temporary_file_path()
        

        result=KManager.predict(image_path,dataset.id)

        

        messages.success(request,'Your image is'+result)

            



class UploadForm(forms.Form):
    label= forms.CharField(max_length=200)
    #image
    image = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/zip'}))
    dataset = forms.ModelChoiceField(queryset= DataSet.objects.all())

    def process(self):
        _label = self.cleaned_data['label']
        dataset = self.cleaned_data['dataset']
        images = self.cleaned_data['image']
        zippath=images.temporary_file_path()
        extractpath=zippath.replace("upload.zip","")+"_f"

        logger.info("managing upload")
        logger.info(zippath)
        logger.info(extractpath)

        #unzip folder
        os.mkdir(extractpath)
        zip_ref = zipfile.ZipFile(zippath, 'r')
        zip_ref.extractall(extractpath)
        zip_ref.close()
        
        onlyfiles = [f for f in listdir(extractpath) if isfile(join(extractpath, f))]

        
        for imagefile in onlyfiles:
            
            item=DataSetItem.objects.create( dataset=dataset,label=_label)
            item.image.save(imagefile,File(open(join(extractpath, imagefile), mode='rb')))

        shutil.rmtree(extractpath)
        messages.success(request,'Your dataset is uploaded')


class DataSetItemForm( forms.ModelForm ):  
    #dataset = forms.ModelMultipleChoiceField(queryset=DataSet.objects.all())
    class Meta:
        model = DataSetItem
        fields = ['label','image','dataset']

class DataSetItemAdmin(admin.ModelAdmin):
    list_display = ('label','image','dataset')
    form=DataSetItemForm
   

class DataSetItemInline(admin.TabularInline):
    model = DataSetItem

admin.site.register(DataSetItem,DataSetItemAdmin)


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






