from django.contrib import admin
from .models import Student, StudentAdminInterface, Exam, ExamAdminInterface, ExamCenter, ExamCenterAdminInterface, Allocation, AllocationAdminInterface

admin.site.register(Student, StudentAdminInterface)
admin.site.register(Exam, ExamAdminInterface)
admin.site.register(ExamCenter, ExamCenterAdminInterface)
admin.site.register(Allocation, AllocationAdminInterface)
# Register your models here.
