import sys
import os
import django

# BASE_DIR = "../../luce_django/luce"

sys.path.append("../../luce_django/luce")
# from accounts.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "lucehome.settings")
# django.setup()

from accounts.models import User

User.objects.all().delete()