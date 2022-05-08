from django.contrib import admin

# Register your models here.
from .models import Step, StepCode


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    pass


@admin.register(StepCode)
class StepCodeAdmin(admin.ModelAdmin):
    pass
