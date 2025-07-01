from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_admin_role = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Get or create admin role
        admin_role, created = Role.objects.get_or_create(
            name='Admin',
            defaults={'is_admin_role': True}
        )
        extra_fields.setdefault('role', admin_role)
        
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'is_admin_role': False}
    )
    registration_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.role:
            user_role, created = Role.objects.get_or_create(
                name='User',
                defaults={'is_admin_role': False}
            )
            self.role = user_role
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username
    

class Category(models.Model):
    category_id=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=100)
    # category_code=models.CharField(max_length=20)

    def __str__(self):
        return self.category_name



class Subject(models.Model):
    subject_id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=100)
    # subject_code=models.CharField(max_length=20)
    category_id=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.subject_name


   
# class Notes(models.Model):
#         CATEGORY_CHOICES = [
#         ('BE_COMPUTER', 'BE COMPUTER'),
#         ('BBA', 'BBA'),
#         ('BCA', 'BCA'),
#         ('BE_CIVIL', 'BE CIVIL'),
#         ('MBA', 'MBA'),
#         ('PLUS_TWO', '+2'),
#         ('OTHERS', 'Others'),
#     ]
#     note_id=models.AutoField(primary_key=True)
#     title=models.CharField(max_length=100)
#     description=models.TextField()
#     notes_file = models.FileField(upload_to='notes/')  # This creates a 'notes' subfolder in MEDIA_ROOT
#     upload_date=models.DateTimeField(auto_now_add=True)
#     user_id=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
#     subject_id=models.ForeignKey(Subject,on_delete=models.CASCADE)
#     download_count=models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return self.title


class Notes(models.Model):
    # CATEGORY_CHOICES = [
    #     ('BE_COMPUTER', 'BE COMPUTER'),
    #     ('BBA', 'BBA'),
    #     ('BCA', 'BCA'),
    #     ('BE_CIVIL', 'BE CIVIL'),
    #     ('MBA', 'MBA'),
    #     ('PLUS_TWO', '+2'),
    #     ('OTHERS', 'Others'),
    # ]
    
    note_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    notes_file = models.FileField(upload_to='notes/')
    upload_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    download_count = models.PositiveIntegerField(default=0)
    # category = models.CharField(
    #     max_length=20,
    #     choices=CATEGORY_CHOICES,
    #     default='BE_COMPUTER'
    # )

    def __str__(self):
        return self.title



# class Role(models.Model):
#     role_id=models.CharField(max_length=1,primary_key=True)
#     role_name=models.CharField(max_length=20)
#     code=models.CharField(max_length=10)
#     def __str__(self):
#         return self.role_name




# class User(AbstractUser):
#     role_id=models.ForeignKey(Role,on_delete=models.CASCADE)
#     def __str__(self):
#         return self.username




class Files(models.Model):
    file_id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to='notes/'
    # media folder ko vitra notes nam ko folder in mange.py sectoin ma
    )
    note_id=models.ForeignKey(Notes,on_delete=models.CASCADE)
