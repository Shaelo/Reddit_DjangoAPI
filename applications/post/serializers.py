from rest_framework import serializers

from applications.post.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email', read_only=True)
    created = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)

    class Meta:
        model = Post
        fields = (
                'id',
                'author',
                'title',
                'created',
                'category',
                'text',
                )
