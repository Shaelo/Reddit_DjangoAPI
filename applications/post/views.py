from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.viewsets import *

from applications.post.filters import Postfilter
from applications.post.permissions import IsAuthor
from applications.post.serializers import *


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000000


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = Postfilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = [AllowAny]
        elif self.action in ['create']:
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthor]
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['GET'], detail=False)
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(title__icontains=q)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk=None):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = Rating.objects.get(post=self.get_object(),
                                     author=request.user)
            obj.rating = request.data['rating']
        except Rating.DoesNotExist:
            obj = Rating(author=request.user,
                         post=self.get_object(),
                         rating=request.data['rating']
                         )

        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        like_obj, _ = Like.objects.get_or_create(post=post, author=request.user)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unlike'
        return Response({'status': status})

    @action(methods=['POST'], detail=True)
    def favorite(self, request, *args, **kwargs):
        post = self.get_object()
        favorite_obj, _ = Favorite.objects.get_or_create(post=post, author=request.user)
        favorite_obj.favorite = not favorite_obj.favorite
        favorite_obj.save()
        status = 'Добавлено в избранное'
        if not favorite_obj.favorite:
            status = 'Удаленно из избранных'
        return Response({'status': status})

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class CommentCreateView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]


class CommentUpdateView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]


class FavoriteListView(ListAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
