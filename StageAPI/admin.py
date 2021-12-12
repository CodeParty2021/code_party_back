from django.contrib import admin

from .models import Stage


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    pass
