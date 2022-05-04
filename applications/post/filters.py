from django_filters import rest_framework as filters
from applications.post.models import Post


class Postfilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = ['title', 'author', 'category']
