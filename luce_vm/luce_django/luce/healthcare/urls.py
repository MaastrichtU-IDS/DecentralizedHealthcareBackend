from django.urls import path
from .views import *

urlpatterns = [
    path('all/', ContractsListView.as_view()),
    path('dataUpload/', UploadDataView.as_view()),
    path('requestAccess/', RequestDatasetView.as_view()),
    path('getLink/', GetLink.as_view()),
    path('<int:id>/', RetrieveContractByUserIDView.as_view()),
    path('search/', SearchContract.as_view()),
    path('deployRegistry/', LuceRegistryView.as_view()),
]
