from re import A
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from django.views.decorators.csrf import csrf_exempt

# from .views import *
from luceview.views import *
# from views import *

# Import settings to access environment variables
from django.conf import settings

urlpatterns = [
    path('docs/', include('sphinxdoc.urls')),
    path('user/', include('accounts.urls')),
    path('contract/', include('luceview.urls')),
    path('admin/', include('luceview.urls')),

    # path('user/register/', UserRegistration.as_view()),
    # path('user/<int:id>/', PublicUserInfoView.as_view()),
    # path('user/authenticated/', PrivateUserInfoView.as_view()),
    # path('user/authenticated/update/', UserUpdateView.as_view()),
    # path('user/all/', UserListView.as_view()),
    # path('user/login/', ObtainAuthToken.as_view()),
    path('admin/deployRegistry/', LuceRegistryView.as_view()),
    # path('contract/all/', ContractsListView.as_view()),
    # path('contract/dataUpload/', UploadDataView.as_view()),
    # path('contract/requestAccess/', RequestDatasetView.as_view()),
    # path('contract/getLink/', GetLink.as_view()),
    # path('contract/<int:id>/', RetrieveContractByUserIDView.as_view()),
    # path('contract/search/', SearchContract.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    # Use local simulated CDN
    # Add the following to urlpatterns
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
