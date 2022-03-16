from django.urls import path, include
from rest_framework import routers

from profiles import views

router = routers.DefaultRouter()
router.register('profiles', views.RegistrationViewSet, "profiles")

urlpatterns = [
    path('', include((router.urls, 'profiles'), namespace='profiles')),
]

