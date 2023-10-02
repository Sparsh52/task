from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(IrisData)
class IrisAdmin(admin.ModelAdmin):
    list_display=('id','sepal_length','sepal_width','petal_length','petal_width','species')