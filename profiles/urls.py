from django.urls import path, include
from rest_framework import routers

from profiles import page_views, registration_views, subscription_views, post_views, admin_views

router = routers.DefaultRouter()
router.register('profiles', registration_views.RegistrationViewSet, "profiles")
router.register('pages', page_views.PageViewSet, "pages")
router.register('subscriptions', subscription_views.SubscriptionViewSet, "subscriptions")
router.register('posts', post_views.PostViewSet, "posts")
router.register('admin-section', admin_views.AdminViewSet, "admins")

urlpatterns = [
    path('', include((router.urls, 'profiles'), namespace='profiles')),
    path('', include((router.urls, 'pages'), namespace='pages')),
    path('', include((router.urls, 'subscriptions'), namespace='subscriptions')),
    path('', include((router.urls, 'posts'), namespace='posts')),
    path('', include((router.urls, 'admin-section'), namespace='admins')),

]

