# from rest_framework import serializers, status
# from rest_framework.response import Response

from eav.serializers import (  # EavEntitySerializer,
    ModelEavDictSerializer,
    ModelEavSerializer,
)

from .models import ExampleModel


class ExampleModelSerializer(ModelEavSerializer):
    class Meta:
        model = ExampleModel
        fields = "__all__"


class ExampleModelEavDictSerializer(ModelEavDictSerializer):
    class Meta:
        model = ExampleModel
        fields = "__all__"
