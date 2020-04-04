from django import template
from django.contrib.auth.models import Group
from django.template import Context, Template
from blog.models import Post
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='sidebar_posts')
def sidebar_posts(arg):
    posts = Post.objects.filter(published=True).order_by('-date_posted')[:5]
    text = '<ul>'
    for post in posts:
        text += f'<li class=""><a href="/post/{post.id}">{post.title}</a></li>'
    text += '</ul>'
    return mark_safe(text)