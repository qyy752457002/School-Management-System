from mini_framework.multi_tenant.registry import tenant_registry
# from mini_framework.web.middlewares.auth import get_tenant
from mini_framework.web.router import root_router

from views.common.common_view import get_tenant_by_code
from views.school.router import routers as schoolrouters
from views.grades.router import routers as grades_router
from views.tasks.router import init_task_router
from views.teachers.router import routers as teachers_router
from views.system.router import routers as systemrouters

from views.students.router import routers as studentrouters
from views.public.router import routers as publicrouters
from views.common.router import routers as commonrouters

def init_router():
    # 从mini_framework.web.mini_app模块中导入app_config
    from mini_framework.web.mini_app import app_config
    # 注册get_tenant_by_code函数到tenant_registry中
    tenant_registry.register_get_tenant(get_tenant_by_code)
    # 设置root_router的根路径为/api/{app_config.name}
    root_router.set_root_prefix(f"/api/{app_config.name}")
    # 将schoolrouters添加到root_router中
    root_router.include_router(schoolrouters())
    # 将grades_router添加到root_router中
    root_router.include_router(grades_router())
    # 将teachers_router添加到root_router中
    root_router.include_router(teachers_router())
    # 将systemrouters添加到root_router中
    root_router.include_router(systemrouters())
    # 将studentrouters添加到root_router中
    root_router.include_router(studentrouters())
    # 将publicrouters添加到root_router中
    root_router.include_router(publicrouters())
    # 将commonrouters添加到root_router中
    root_router.include_router(commonrouters())
    
    # root_router.include_router(init_task_router())
    init_task_router()


