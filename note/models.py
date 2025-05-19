from django.db import models
from django.conf import settings 
# garna parxa to make user id as foreign key

from django.contrib.auth.models import AbstractUser

# Create your models here.
class Category(models.Model):
    category_id=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=100)
    category_code=models.CharField(max_length=20)

    def __str__(self):
        return self.category_name



class Subject(models.Model):
    subject_id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=100)
    subject_code=models.CharField(max_length=20)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.subject_name


    
class Notes(models.Model):
    note_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    description=models.TextField()
    notes_file=models.FileField(null=True)
    upload_date=models.DateField(auto_now_add=True)
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subject_id=models.ForeignKey(Subject,on_delete=models.CASCADE)
    download_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title



class Role(models.Model):
    role_id=models.CharField(max_length=1,primary_key=True)
    role_name=models.CharField(max_length=20)
    code=models.CharField(max_length=10)
    def __str__(self):
        return self.role_name




class User(AbstractUser):
    role_id=models.ForeignKey(Role,on_delete=models.CASCADE)
    def __str__(self):
        return self.username




class Files(models.Model):
    file_id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to='notes/'
    # media folder ko vitra notes nam ko folder in mange.py sectoin ma 
    )
    note_id=models.ForeignKey(Notes,on_delete=models.CASCADE)