from mini_framework.web.router import root_router
from views.tests.router import routers
from views.school.router import routers as schoolrouters
from views.grades.router import routers as grades_router


def init_router():
    from mini_framework.web.mini_app import app_config
    root_router.set_root_prefix(f"/api/{app_config.name}")
    root_router.include_router(routers())
    root_router.include_router(schoolrouters())
    root_router.include_router(grades_router())
