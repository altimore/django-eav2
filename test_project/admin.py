from django.contrib import admin

from eav.admin import BaseEntityAdmin
from eav.forms import BaseDynamicEntityForm

from .models import ExampleModel


class PatientAdminForm(BaseDynamicEntityForm):
    model = ExampleModel


class ExampleModelAdmin(BaseEntityAdmin):
    form = PatientAdminForm


admin.site.register(ExampleModel)
