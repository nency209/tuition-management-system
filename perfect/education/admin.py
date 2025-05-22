from django.contrib import admin 
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.urls import path
from django.shortcuts import render
from . import views

# from education.models import Post  # Replace with your models

class admin_(admin.ModelAdmin):
    list_display=['name','email']
    list_filter=['name','email']
    search_fields=['name','email']
admin.site.register(Author,admin_)

# -------------------

# --------------------






class notice_(admin.ModelAdmin):
    list_display=['date','name','msg']
admin.site.register(notice,notice_)

admin.site.register(inquiry)
# admin.site.register(payment)
admin.site.register(Class)
admin.site.register(gallery)
admin.site.register(student)
admin.site.register(Subjects)
admin.site.register(teacher)
admin.site.register(batch_time_table)