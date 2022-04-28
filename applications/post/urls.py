from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.post.views import *

router = DefaultRouter()
router.register('', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListView.as_view()),
]
