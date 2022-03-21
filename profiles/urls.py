from django.urls import path, include
from rest_framework import routers

from profiles import views

router = routers.DefaultRouter()
router.register('profiles', views.RegistrationViewSet, "profiles")
router.register('pages', views.PageViewSet, "pages")
router.register('subscriptions', views.SubscriptionViewSet, "subscriptions")

urlpatterns = [
    path('', include((router.urls, 'profiles'), namespace='profiles')),
    path('', include((router.urls, 'pages'), namespace='pages')),
    path('', include((router.urls, 'subscriptions'), namespace='subscriptions')),

]

