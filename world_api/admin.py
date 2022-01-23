from django.contrib import admin

from .models import World


@admin.register(World)
class WorldAdmin(admin.ModelAdmin):
    pass
