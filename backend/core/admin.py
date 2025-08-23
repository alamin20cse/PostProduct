from django.contrib import admin
from .models import User,Post,Product,Payment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display='__all__',
    admin.site.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display='__all__',
    admin.site.register(Post)
class ProductAdmin(admin.ModelAdmin):
    list_display='__all__',
    admin.site.register(Product)
class PaymentAdmin(admin.ModelAdmin):
    list_display='__all__',
    admin.site.register(Payment)
