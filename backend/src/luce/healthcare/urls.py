from django.urls import path
from .views import *

urlpatterns = [
    path('all/', ContractsListView.as_view()),
    path('dataUpload/', UploadDataView.as_view(), name='upload_data_view'),
    path('requestAccess/',
         RequestDatasetView.as_view(),
         name="request_dataset_view"),
    path('getLink/', GetLink.as_view()),
    path('<int:id>/', RetrieveContractByUserIDView.as_view()),
    path('search/', SearchContract.as_view()),
    path('deployRegistry/',
         LuceRegistryView.as_view(),
         name='deploy_registry_view'),
]
