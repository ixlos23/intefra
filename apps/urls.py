from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegisterCreateAPIView, LoginAPIView, FilmCreateAPIView, FilmListAPIView

urlpatterns = [
    path('register/', RegisterCreateAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('film/', FilmCreateAPIView.as_view(), name='film'),
    path('films/', FilmListAPIView.as_view(), name='film-list'),
]
