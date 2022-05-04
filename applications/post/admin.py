from django.contrib import admin
from applications.post.models import *

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Favorite)


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 5


@admin.register(Post)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInAdmin]



