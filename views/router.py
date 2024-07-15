from mini_framework.web.router import root_router
from views.school.router import routers as schoolrouters
from views.grades.router import routers as grades_router
from views.tasks.router import init_task_router
from views.teachers.router import routers as teachers_router
from views.system.router import routers as systemrouters

from views.students.router import routers as studentrouters
from views.public.router import routers as publicrouters


def init_router():
    from mini_framework.web.mini_app import app_config
    root_router.set_root_prefix(f"/api/{app_config.name}")
    root_router.include_router(schoolrouters())
    root_router.include_router(grades_router())
    root_router.include_router(teachers_router())
    root_router.include_router(systemrouters())
    root_router.include_router(studentrouters())
    root_router.include_router(publicrouters())
    root_router.include_router(init_task_router())

