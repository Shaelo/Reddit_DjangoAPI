from rest_framework import serializers

from applications.post.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    added = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating',)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    created = serializers.DateTimeField(format='%d.%m.%Y %H:%M', read_only=True)
    comment = CommentSerializer(required=False, many=True)
    image = ImageSerializer(many=True, read_only=True)
    rating = RatingSerializer(required=False, many=True)
    like = LikeSerializer(required=False, many=True)

    class Meta:
        model = Post
        fields = (
                'id',
                'author',
                'title',
                'image',
                'created',
                'category',
                'text',
                'rating',
                'comment',
                'like',
                )

    def create(self, validated_data):
        request = self.context.get('request')
        image_data = request.FILES
        post = Post.objects.create(**validated_data)
        for image in image_data.getlist('image'):
            Image.objects.create(post=post, image=image)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_result = 0
        for i in instance.rating.all():
            rating_result += int(i.rating)
        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation['rating'] = rating_result / instance.rating.all().count()
        representation['like'] = instance.like.filter(like=True).count()
        return representation


