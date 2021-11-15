from re import A
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from django.views.decorators.csrf import csrf_exempt



from .views import *
from rest_framework.authtoken import views


# Import settings to access environment variables 
from django.conf import settings


urlpatterns = [
    path('user/register/', UserRegistration.as_view()),
    path('user/<int:id>/', PublicUserInfoView.as_view()),
    path('user/authenticated/', PrivateUserInfoView.as_view()),
    path('user/authenticated/update/', UserUpdateView.as_view()),
    path('user/all/', UserListView.as_view()),
    path('user/login/', views.obtain_auth_token),

    path('deployContract/', ContractView.as_view())
    ]

urlpatterns = format_suffix_patterns(urlpatterns)


if settings.DEBUG:
    # Use local simulated CDN
    # Add the following to urlpatterns
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
