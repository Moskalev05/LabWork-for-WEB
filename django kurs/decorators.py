from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_admin():
            return HttpResponseForbidden("У вас нет прав для доступа к этой странице")
        return view_func(request, *args, **kwargs)
    return _wrapped_view