from typing import List

from fastapi import Depends, Body, Query
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView

from rules.common.sync_rule import SyncRule
from rules.school_rule import SchoolRule
from rules.planning_school_rule import PlanningSchoolRule
from rules.teacher_import_rule import TeacherImportRule
from rules.teachers_rule import TeachersRule
from views.models.school_and_teacher_sync import SchoolSyncQueryModel, SupervisorSyncQueryModel, \
    SupervisorSyncQueryReModel


class SchoolTeacherView(BaseView):
    def __init__(self):
        super().__init__()
        self.sync_rule = get_injector(SyncRule)
        self.teacher_import_rule = get_injector(TeacherImportRule)
        self.teacher_rule = get_injector(TeachersRule)
        self.school_rule = get_injector(SchoolRule)
        self.planning_school_rule = get_injector(PlanningSchoolRule)

    async def page_school(self, query_model=Depends(SchoolSyncQueryModel),
                          page_request=Depends(PageRequest)) -> PaginatedResponse:
        res = await self.sync_rule.query_sync_school_with_page(query_model, page_request)
        return res

    async def page_teachers(self, query_model=Depends(SupervisorSyncQueryModel),
                            page_request=Depends(PageRequest)) -> PaginatedResponse:
        res = await self.sync_rule.query_sync_teacher_with_page(query_model, page_request)
        return res

    async def get_all_teachers_id_list(self):
        return await self.teacher_rule.get_all_teachers_id_list()

    async def post_sync_teacher(self,
                                teacher_id_number_list: List[str] | None = Body(None, title="",
                                                                                description="身份证件号",
                                                                                examples=['3425301994'])) -> List[
        SupervisorSyncQueryReModel]:
        res = await self.sync_rule.get_sync_teacher(teacher_id_number_list)
        print(res)
        return res

    async def post_sync_school(self, unique_code_list: List[str] | None = Body([], title="",
                                                                               description="统一社会信用代码",
                                                                               examples=['3425301994'])) -> List:
        res = await self.sync_rule.get_sync_school(unique_code_list)
        return res

    async def get_all_school(self):
        res = await self.sync_rule.get_all_school()
        return res

    async def post_school_by_school_no(self, unique_code_list: List[str] | None = Body([], title="",
                                                                                       description="学校代码",
                                                                                       examples=[
                                                                                           '3425301994'])) -> List:
        res = await self.sync_rule.get_school_by_school_no(unique_code_list)
        return res

    async def get_sync_student(self, school_no: str = Query(..., title="学校代码",
                                                            description="学校代码", example='3425301994')):
        res = await self.sync_rule.get_sync_student_by_school_no(school_no)
        return res

    async def get_sync_teacher_to_art(self, school_no: str = Query(..., title="学校代码",
                                                                   description="学校代码", example='3425301994')):
        res = await self.sync_rule.get_sync_teacher_to_art(school_no)
        return res

    async def get_import_teachers_save_test(self, org_id: int = Query(..., title="组织id", description="组织id",
                                                                      example=123)):
        result = await self.teacher_import_rule.import_teachers_save_test(org_id)
        return result

    async def post_single_teacher_to_org_center(self,
                                                teacher_id: int | str = Body(..., title="教师编号",
                                                                             description="教师编号",
                                                                             example=123)):
        teacher_id = int(teacher_id)
        res = await self.teacher_rule.send_teacher_to_org_center(teacher_id)
        return res

    async def post_teacher_list_to_org_center(self, teacher_id_list: List[str] | None = Body(None, title="",
                                                                                             description="身份证件号",
                                                                                             examples=['3425301994'])):
        for teacher_id in teacher_id_list:
            try:
                await self.teacher_rule.send_teacher_to_org_center(int(teacher_id))
            except Exception as e:
                print(f'编号{teacher_id}的发生错误{e}')
                return f'编号{teacher_id}的发生错误{e}'

    async def post_school_list_to_org_center(self, school_no_list: List[str] | None = Body([], title="",
                                                                                           description="学校代码",
                                                                                           examples=['3425301994'])):
        """
        为了让一期学校同步到二期，并且能够同步到组织中心
        """
        for school_no in school_no_list:
            try:
                await self.school_rule.send_school_to_org_center_by_school_no(school_no)
            except Exception as e:
                print(f'编号{school_no}的发生错误{e}')
                return f'编号{school_no}的发生错误{e}'
        return 'success'


    async def post_planning_school_list_to_org_center(self, planning_school_no_list: List[str] | None = Body([], title="",
                                                                                                             description="学校代码",
                                                                                                             examples=[
                                                                                                                 '3425301994'])):
        """
        为了让一期学校同步到二期，并且能够同步到组织中心
        """
        for planning_school_code in planning_school_no_list:
            try:
                await self.planning_school_rule.send_planning_school_to_org_center_by_school_no(planning_school_code)
            except Exception as e:
                print(f'编号{planning_school_code}的发生错误{e}')
                return f'编号{planning_school_code}的发生错误{e}'
        return 'success'

    async def get_all_planning_school_no(self):
        res = await self.planning_school_rule.get_all_planning_school_no()
        return res

    async def get_all_school_no(self):
        res = await self.school_rule.get_all_school_no()
        return res

