from mini_framework.web.router import Router

from views.models.teachers import Teachers
from views.students.current_students_view import CurrentStudentsView
from views.students.graduation_students_view import GraduationStudentsView

from views.students.newstudents_view import  NewsStudentsView



def routers():
    router = Router()
    router.include_api_view_class(NewsStudentsView, "/v1/news-students-view",  description="新生入学管理")
    router.include_api_view_class(CurrentStudentsView, "/v1/current-student",  description="在校生管理")
    router.include_api_view_class(GraduationStudentsView, "/v1/graduation-student",  description="毕业生管理")


    return router
