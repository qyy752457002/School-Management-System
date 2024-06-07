from mini_framework.web.router import Router

from views.school.campus_view import CampusView
from views.school.classes_view import ClassesView
from views.school.course_view import CourseView
from views.school.institution_view import InstitutionView
from views.school.leader_info_view import LeaderInfoView
from views.school.major_view import MajorView
from views.school.organization_view import OrganizationView
from views.school.planning_school_view import PlanningSchoolView
from views.school.school_view import SchoolView


def routers():
    router = Router()
    router.include_api_view_class(OrganizationView, "/v1/organization",   description="组织架构管理")
    router.include_api_view_class(SchoolView, "/v1/school",   description="学校管理")
    router.include_api_view_class(LeaderInfoView, "/v1/leaderinfo",   description="领导管理")


    router.include_api_view_class(PlanningSchoolView, "/v1/planningschool",   description="规划校管理")

    router.include_api_view_class(InstitutionView, "/v1/institution",   description="行政事业单位管理")
    router.include_api_view_class(CampusView, "/v1/campus",   description="校区管理")

    router.include_api_view_class(ClassesView, "/v1/classes",   description="班级管理")

    router.include_api_view_class(MajorView, "/v1/major",   description="专业管理")
    router.include_api_view_class(CourseView, "/v1/course",   description="课程管理")

    return router
