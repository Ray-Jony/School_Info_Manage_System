from django.contrib import admin
from .models import 老师


# Register your models here.

class teacher_admin(admin.ModelAdmin):
    list_display = ['id', '老师姓名', '老师电话']
    list_per_page = 10


admin.site.register(老师, teacher_admin)



