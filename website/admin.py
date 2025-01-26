from django.contrib import admin

# Register your models here.
from .models import Store
from .models import Medicine

admin.site.register(Store)
admin.site.register(Medicine)