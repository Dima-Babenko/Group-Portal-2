from django.contrib import admin
from .models import Subject, Student, Schedule, Grade

admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Schedule)
admin.site.register(Grade)