from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .views import (
    EavAttributeViewSet,
    EavEnumGroupViewSet,
    EavEnumValueViewSet,
    ExampleModelViewSet,
)

router = routers.DefaultRouter()

router.register(prefix="attribute", viewset=EavAttributeViewSet)
router.register(prefix="enum_group", viewset=EavEnumGroupViewSet)
router.register(prefix="enum_value", viewset=EavEnumValueViewSet)
router.register(prefix="example_model", viewset=ExampleModelViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("admin/", admin.site.urls),
]
