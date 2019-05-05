from django.contrib.auth.models import User, Group
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.utils import timezone
from management.models import DataSet,DataSetItem



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class DataSetItemSerializer(serializers.HyperlinkedModelSerializer):
    image = Base64ImageField()
    dataset=   serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    class Meta:
        model = DataSetItem

        # Fields to expose via API
        fields = ('label', 'image', 'dataset')

    # def create(self, validated_data):
    #     image = validated_data.pop('image')
    #     dataset=validated_data.pop('dataset')
    #     label=validated_data.pop('label')
    #     ret = DataSetItem.objects.create(image=image, label=label, dataset=dataset)
    #     return ret


class DataSetSerializer(serializers.HyperlinkedModelSerializer):  
   
    class Meta:
        model = DataSet
        fields = ('name', 'process')


class TestItemSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    class Meta:
        model = DataSetItem
        # Fields to expose via API
        fields = ( 'image', 'dataset')
