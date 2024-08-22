from functools import wraps

from mini_framework.web.request_context import request_context_manager

from business_exceptions.auth import NoPermissionError
from rules.common.common_rule import verify_auth_by_obj_and_act
from views.common.common_view import system_config


def require_role_permission(role: str, action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            v = await verify_auth_by_obj_and_act(role, action)
            is_permission_verify = system_config.system_config.get("permission_verify")
            print('permission verify',  is_permission_verify)

            if not v:
                print('no permission', role, action,)
                if is_permission_verify:
                    raise NoPermissionError()
            return await func(*args, **kwargs)
        return wrapper
    return decorator
