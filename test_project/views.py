from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from eav.models import Attribute, EnumGroup, EnumValue
from eav.serializers import (
    AttributeSerializer,
    EnumGroupSerializer,
    EnumValueSerializer,
)

from .models import ExampleModel
from .serializers import ExampleModelEavDictSerializer, ExampleModelSerializer


class EavAttributeViewSet(viewsets.ModelViewSet):
    model = Attribute
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     return Entity.objects.filter(entity__object_id=self.kwargs["pk"])


class EavEnumGroupViewSet(viewsets.ModelViewSet):
    model = EnumGroup
    queryset = EnumGroup.objects.all()
    serializer_class = EnumGroupSerializer
    permission_classes = [AllowAny]


class EavEnumValueViewSet(viewsets.ModelViewSet):
    model = EnumValue
    queryset = EnumValue.objects.all()
    serializer_class = EnumValueSerializer
    permission_classes = [AllowAny]


class ExampleModelViewSet(viewsets.ModelViewSet):
    model = ExampleModel
    queryset = ExampleModel.objects.all()
    serializer_class = ExampleModelEavDictSerializer
    permission_classes = [AllowAny]
