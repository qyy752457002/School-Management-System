from mini_framework.multi_tenant.registry import tenant_registry
from mini_framework.web.middlewares.auth import get_tenant
from mini_framework.web.router import root_router
from views.school.router import routers as schoolrouters
from views.grades.router import routers as grades_router
from views.tasks.router import init_task_router
from views.teachers.router import routers as teachers_router
from views.system.router import routers as systemrouters

from views.students.router import routers as studentrouters
from views.public.router import routers as publicrouters
from views.common.router import routers as commonrouters


def init_router():
    from mini_framework.web.mini_app import app_config
    tenant_registry.register_get_tenant(get_tenant)
    root_router.set_root_prefix(f"/api/{app_config.name}")
    root_router.include_router(schoolrouters())
    root_router.include_router(grades_router())
    root_router.include_router(teachers_router())
    root_router.include_router(systemrouters())
    root_router.include_router(studentrouters())
    root_router.include_router(publicrouters())
    root_router.include_router(commonrouters())
    # root_router.include_router(init_task_router())
    init_task_router()


