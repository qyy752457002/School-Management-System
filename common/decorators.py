from functools import wraps

from business_exceptions.auth import NoPermissionError
from rules.common.common_rule import verify_auth_by_obj_and_act


def require_role_permission(role: str, action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # v = await verify_auth_by_obj_and_act(role, action)
            # if not v:
            #     raise NoPermissionError()
            return await func(*args, **kwargs)
        return wrapper
    return decorator
