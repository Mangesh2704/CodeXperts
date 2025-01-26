from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Store(models.Model):
    store_id = models.AutoField
    store_code = models.CharField(max_length=50)
    store_state = models.CharField(max_length=100)
    store_district = models.CharField(max_length=50)
    store_address = models.CharField(max_length=300)
    store_pincode = models.CharField(max_length=10)
    store_contact = models.CharField(max_length=50)

    def __str__(self):
        return self.store_code
    
class Medicine(models.Model):
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)  # New field for images
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=50, choices=[('Volunteer', 'Volunteer'), ('Business Owner', 'Business Owner')], default='Volunteer')  # Set default here
    
    def __str__(self):
        return f"Profile of {self.user.username}"
