from django.contrib import admin


# Include Datasets in admin interface 
from .models import Dataset
admin.site.register(Dataset)