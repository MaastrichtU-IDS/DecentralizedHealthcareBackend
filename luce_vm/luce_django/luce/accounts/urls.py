from django.urls import path
# from views import *
from .views import *

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('<int:id>/', PublicUserInfoView.as_view()),
    path('authenticated/', PrivateUserInfoView.as_view()),
    path('authenticated/update/', UserUpdateView.as_view()),
    path('all/', UserListView.as_view()),
    path('login/', ObtainAuthToken.as_view()),
]