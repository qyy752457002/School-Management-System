from mini_framework.web.views import BaseView

from rules.common.common_rule import send_permission_to_front


class PermissionView(BaseView):
    async def get_permission(self):
        return await send_permission_to_front()
