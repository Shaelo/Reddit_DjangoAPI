from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.post.views import *

router = DefaultRouter()
router.register('', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('category/', CategoryListView.as_view()),
    path('category/create/', CategoryCreateView.as_view()),
    path('comment/add/', CommentCreateView.as_view()),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view()),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view()),
    path('favorites/', FavoriteListView.as_view()),
]
