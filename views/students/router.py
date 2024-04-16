from mini_framework.web.router import Router

from views.models.teachers import Teachers

from views.students.newstudents_view import  NewsStudentsView



def routers():
    router = Router()
    router.include_api_view_class(NewsStudentsView, "/v1/NewsStudentsView",  description="新生入学管理")

    return router
