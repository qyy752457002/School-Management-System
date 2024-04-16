from mini_framework.web.router import Router

from views.models.grades import Grades

from views.grades.grades_view import GradesView



def routers():
    router = Router()
    router.include_api_view_class(GradesView, "/v1/grades", response_cls=Grades , description="年级管理")
    return router
