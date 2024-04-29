from mini_framework.web.router import Router

from views.models.teachers import Teachers
from views.students.current_students_view import CurrentStudentsView, CurrentStudentsBaseInfoView, CurrentStudentsFamilyView
from views.students.graduation_students_view import GraduationStudentsView

from views.students.newstudents_view import NewsStudentsView, NewsStudentsInfoView,NewsStudentsFamilyInfoView
from views.students.student_inner_transaction_view import StudentInnerTransactionView


def routers():
    router = Router()
    router.include_api_view_class(NewsStudentsView, "/v1/news-students-view", description="新生入学管理")
    router.include_api_view_class(CurrentStudentsView, "/v1/current-student", description="在校生管理")
    router.include_api_view_class(GraduationStudentsView, "/v1/graduation-student", description="毕业生管理")
    router.include_api_view_class(NewsStudentsInfoView, "/v1/news-students-info", description="新生基本信息管理")
    router.include_api_view_class(NewsStudentsFamilyInfoView, "/v1/news-students-family-info", description="新生家庭信息管理")
    router.include_api_view_class(CurrentStudentsBaseInfoView, "/v1/current-students-base-info", description="在校生基本信息管理")
    router.include_api_view_class(StudentInnerTransactionView, "/v1/current-students-inner-transaction", description="在校生校内异动")
    router.include_api_view_class(CurrentStudentsFamilyView, "/v1/current-students-family-info", description="在校生家庭信息管理")

    return router
