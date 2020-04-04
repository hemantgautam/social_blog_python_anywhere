from django.contrib import admin
from .models import Post, PostComment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published']
    search_fields = ['title', 'author']


admin.site.register(Post, PostAdmin)
admin.site.register(PostComment)
