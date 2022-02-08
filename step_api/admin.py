from django.contrib import admin

# Register your models here.
from .models import Step


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    pass
