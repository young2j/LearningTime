from functools import wraps

from flask import abort
from flask_login import current_user

from app.models import Permission


def permissions_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args,**kwargs):
            if not current_user.can(perm):
                abort(403)
            return f(*args,**kwargs)
        return decorated_func
    return decorator

def admin_required(f):
    return permissions_required(Permission.ADMIN)(f)