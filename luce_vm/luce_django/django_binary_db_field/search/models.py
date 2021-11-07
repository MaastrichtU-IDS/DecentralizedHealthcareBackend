from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class SearchQuery(models.Model):
	query = models.CharField(max_length=220)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	timestamp = models.DateTimeField(auto_now_add=True)
