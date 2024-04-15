from mini_framework.web.views import BaseView

from views.models.test import ApplicationInfo


class TestView(BaseView):
    async def get(self):
        return ApplicationInfo(
            name="School Management System", version="1.0.0",
            description="A school management system", author="Lfun technical",
            author_email="cloud@lfun.cn", copyright="Copyright © 2024 Lfun technical"
        )
