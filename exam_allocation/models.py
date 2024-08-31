import time
from django.contrib import admin
from django.db import models

# Create your models here.    
class Exam(models.Model):
    exam_id = models.IntegerField(primary_key=True)
    exam_name = models.CharField(max_length=100)
    exam_date = models.DateField()
    instruction = models.TextField()
    
    def __str__(self):
        return self.exam_name
    
    
class ExamCenter(models.Model):
    exam_center_id = models.IntegerField(primary_key=True)
    center_name = models.CharField(max_length=100)
    total_capacity = models.IntegerField()
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.center_name
    
class Student(models.Model):
    student_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=1000, null=True, blank=True)
    aadhar_number = models.CharField(max_length=12)
    date_of_birth = models.DateField()
    exam_center_choice = models.ForeignKey(ExamCenter, on_delete=models.CASCADE)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        roll_string = str(self.exam_id.pk)+str(self.exam_center_choice.pk)+time.monotonic().__str__().replace('.','')
        self.roll_number = roll_string
        super(Student, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.first_name+" "+self.last_name + " : " + str(self.exam_center_choice)
            
class Allocation(models.Model):
    exam_name = models.CharField()
    exam_center_id = models.IntegerField()
    roll_number = models.CharField()
    exam_date = models.DateField()
    exam_time = models.CharField()
    
    def __str__(self):
        return str(self.exam_center_id)+ " : " +self.roll_number + " : "+self.exam_time
    
class StudentAdminInterface(admin.ModelAdmin):
    list_per_page = 10
    
class ExamCenterAdminInterface(admin.ModelAdmin):
    list_per_page = 10
    
class ExamAdminInterface(admin.ModelAdmin):
    list_per_page = 10
    
class AllocationAdminInterface(admin.ModelAdmin):
    list_per_page = 10
    

    
    
    
    