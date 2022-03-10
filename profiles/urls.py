from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('innotter', views.RegistrationViewSet, "innotter")

urlpatterns = []

urlpatterns += router.urls
