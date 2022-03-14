from django.urls import path, include
from rest_framework import routers

from profiles import views

app_name = 'profiles'
router = routers.DefaultRouter()
router.register('innotter', views.RegistrationViewSet, "innotter")

urlpatterns = [
    path('api/', include((router.urls, 'innotter'), namespace='profiles')),
]

