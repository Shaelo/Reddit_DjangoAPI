from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(max_length=25, primary_key=True)

    def __str__(self):
        return self.slug


class Post(models.Model):
    author = models.ForeignKey(User, related_name='post', on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    category = models.ForeignKey(Category, related_name='post', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} {self.text}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    added = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField()

    def __str__(self):
        return f'Пользователь {self.author} добавил комментарий к посту {self.post}'


class Image(models.Model):
    image = models.ImageField(upload_to='image')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField('like', default=False)

    def __str__(self):
        return f'{self.author}'


class Favorite(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorite')
    favorite = models.BooleanField('favorite', default=False)
