from mini_framework.web.router import Router

from views.public.classes_view import ClassesView
from views.public.current_students_view import CurrentStudentsView
from views.public.newstudents_view import NewsStudentsInfoView
from views.public.tenant_view import TenantView
from views.school.campus_view import CampusView
from views.school.course_view import CourseView
from views.school.institution_view import InstitutionView
from views.school.leader_info_view import LeaderInfoView
from views.school.major_view import MajorView
from views.school.organization_member_view import OrganizationMemberView
from views.school.organization_view import OrganizationView
from views.school.planning_school_view import PlanningSchoolView
from views.school.school_view import SchoolView
from views.school.subject_view import SubjectView
from views.public.school_and_teacher_sync_view import SchoolTeacherView


def routers():
    router = Router()
    router.include_api_view_class(NewsStudentsInfoView, "/v1/public/current-student", description="已分班生管理")
    router.include_api_view_class(CurrentStudentsView, "/v1/public/new-student", description="在校生管理")
    router.include_api_view_class(ClassesView, "/v1/public/class", description="班级管理")
    router.include_api_view_class(SchoolTeacherView, "/v1/sync", description="同步管理")
    router.include_api_view_class(TenantView, "/v1/tenant", description="同步租户的信息")


    return router
