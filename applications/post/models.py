from django.contrib.auth import get_user_model
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

