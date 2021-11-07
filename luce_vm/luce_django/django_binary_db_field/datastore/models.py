from django.db import models

# Import user model
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Module for combined queries
from django.db.models import Q

# Import Custom QuerySet and Manager
from datastore.managers import DatasetQuerySet, DatasetManager


class Dataset(models.Model):
    # These fields are provided by data provider
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    license         = models.IntegerField() # encoded as integer
    file            = models.FileField(upload_to='files/', blank=True, null=True)
    file_binary     = models.BinaryField(blank=True, null=True, editable = True)

    # These fields are populated automatically
    owner           = models.CharField(max_length=120) # owner username/email
    owner_address   = models.CharField(max_length=180) # msg.sender

    # These fields are populated when a dataset is published
    contract_address= models.CharField(max_length=180) # address of smart contract
    published       = models.BooleanField(default = False)

    # Keep track of access rights
    access_granted  = models.ManyToManyField(User, related_name='datasets_accessible')
    
    # Useful information when dataset was first uploaded and last updated..
    created_by      = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL, related_name='datasets_owned')
    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    # Update to use custom model manager
    objects         = DatasetManager()

    # Dataset object methods
    def get_absolute_url(self):
        return f"/data/{self.pk}"

    def get_edit_url(self):
        return f"/data/{self.pk}/edit"

    def get_delete_url(self):
        return f"/data/{self.pk}/delete"

    def get_publish_url(self):
        return f"/data/{self.pk}/publish"

    def get_request_access_url(self):
        return f"/data/{self.pk}/request"

    # Subclass with meta information like ordering
    class Meta:
        # The negative value means that newest datasets will show up first
        ordering = ['-updated', '-timestamp']




