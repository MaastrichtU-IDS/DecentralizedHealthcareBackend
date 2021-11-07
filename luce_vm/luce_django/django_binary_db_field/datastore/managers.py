from django.db import models

# Module for combined queries
from django.db.models import Q

# Custom QuerySet methods
class DatasetQuerySet(models.QuerySet):
    def search(self, query):
        lookup = (
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(license__icontains=query)
                )
        return self.filter(lookup)

    def published(self):
        return self.filter(published=True)

# Custom Model Manager
class DatasetManager(models.Manager):
    def get_queryset(self):
        return DatasetQuerySet(self.model, using=self._db)

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)

    def published(self):    
       return self.get_queryset().published()  



