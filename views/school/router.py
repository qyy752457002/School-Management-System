from mini_framework.web.router import Router

from views.models.school import School
from views.models.test import ApplicationInfo
from views.school.school_view import SchoolView
from views.tests.test_view import TestView
from views.models.planning_school import PlanningSchool
from views.school.planning_school_view import PlanningSchoolView
from views.models.institutions import Institutions
from views.school.institution_view import InstitutionView


def routers():
    router = Router()
    router.include_api_view_class(SchoolView, "/v1/school",   description="学校管理")

    router.include_api_view_class(PlanningSchoolView, "/v1/planningschool",   description="规划校管理")

    router.include_api_view_class(InstitutionView, "/v1/institution",   description="行政事业单位管理")



    return router
