from django.contrib import admin

from .models import Code,ResultCode,Result


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass

@admin.register(ResultCode)
class ResultCodeAdmin(admin.ModelAdmin):
    pass

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass