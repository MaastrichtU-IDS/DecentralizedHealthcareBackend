from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from healthcare.views import *

# Import settings to access environment variables
from django.conf import settings


# Create a schema view for the OpenAPI docs
schema_view = get_schema_view(
    openapi.Info(
        title="LUCE blockchain API",
        default_version="v1",
        description="API for the LUCE blockchain",
        terms_of_service="https://github.com/MaastrichtU-IDS/DecentralizedHealthcareBackend/blob/master/LICENSE.md",
        contact=openapi.Contact(email="contact@yourcompany.com"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # TODO: the frontend code only uses calls to /user/ and /contract/ endpoints
    path('user/', include('accounts.urls')),
    path('contract/', include('healthcare.urls')),

    path('admin/', include('healthcare.urls')),
    path('admin/deployRegistry/', LuceRegistryView.as_view()),

    path('', RedirectView.as_view(url='/docs/', permanent=True)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # path('user/register/', UserRegistration.as_view()),
    # path('user/<int:id>/', PublicUserInfoView.as_view()),
    # path('user/authenticated/', PrivateUserInfoView.as_view()),
    # path('user/authenticated/update/', UserUpdateView.as_view()),
    # path('user/all/', UserListView.as_view()),
    # path('user/login/', ObtainAuthToken.as_view()),
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
