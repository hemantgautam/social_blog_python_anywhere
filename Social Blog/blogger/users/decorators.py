from django.shortcuts import render, redirect


def logout_require(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return function(request, *args, **kwargs)
    return wrap