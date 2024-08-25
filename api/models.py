from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        username = email  # Use email as username if needed
        
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name,
                           role=role, **extra_fields)
        
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user

class User(AbstractUser):
    email = models.EmailField(unique=True)
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employee", "Employee"),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='employee')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    objects = CustomUserManager()

    def __str__(self):
        return self.email 

class Inventory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField(max_length=10,)
    quantity = models.IntegerField()

class Transaction(models.Model):
    inventory=models.ForeignKey(Inventory,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=255)
    date=models.DateField(default=date.today)
    time=models.TimeField(auto_now_add=True)