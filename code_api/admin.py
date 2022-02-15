from django.contrib import admin

from .models import ProgrammingLanguage, Code


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass
