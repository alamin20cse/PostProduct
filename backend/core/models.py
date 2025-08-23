from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    is_blocked = models.BooleanField(default=False)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    details = models.TextField()
    photo = models.ImageField(upload_to='post_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    size = models.CharField(max_length=100)
    details = models.TextField()
    photo = models.ImageField(upload_to='product_photos/')
    created_at = models.DateTimeField(auto_now_add=True)











# models.py


class Payment(models.Model):
    email = models.EmailField()
    price = models.FloatField()
    transactionId = models.CharField(max_length=255)
    date = models.DateTimeField()
    menuItemIds = models.CharField(max_length=255)  # single id or comma separated
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return self.transactionId












