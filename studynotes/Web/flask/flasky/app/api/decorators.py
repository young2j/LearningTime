from functools import wraps
from flask import abort,g
from app.models import Permission
from .errors import forbidden

def permissions_required(perm):
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            if not g.current_user.can(perm):
                return forbidden('Insuficient Permission.')
            return f(*args, **kwargs)
        return decorated_func
    return decorator


def admin_required(f):
    return permissions_required(Permission.ADMIN)(f)
