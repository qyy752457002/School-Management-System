from mini_framework.web.views import BaseView

from views.models.teachers import NewTeacher, TeacherInfo
from fastapi import Query, Depends
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse

from sqlalchemy import select
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from models.teachers import Teacher
from rules.teachers_rule import TeachersRule
from views.models.teachers import Teachers, TeacherInfo
from rules.teachers_info_rule import TeachersInfoRule


class NewTeachersView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_info_rule = get_injector(TeachersInfoRule)

    # 新增教职工登记信息
    async def post_newteacher(self, teachers: Teachers):
        print(teachers)
        res = await self.teacher_rule.add_teachers(teachers)
        return res

    # 查询单个教职工登记信息
    async def get_newteacher(self, id: str = Query(None, title="教师编号", description="教师编号", min_length=1)):
        res = await self.teacher_rule.get_teachers_by_id(id)
        return res

    # 编辑新教职工登记信息
    async def put_newteacher(self, teachers: Teachers):
        print(teachers)
        res = await self.teacher_rule.update_teachers(teachers)
        return res

    # 分页查询

    async def page(self, condition: NewTeacher = Depends(NewTeacher), page_request=Depends(PageRequest),
                   # teacher_name: str = Query(None, title="教师名称", description="教师名称", min_length=1, max_length=20, example='张三'),
                   # teacher_gender: str = Query(None, title="教师性别", description="教师性别", min_length=1, max_length=20, example='男'),
                   # teacher_id_number: str = Query(None, title="证件类型", description="证件类型", min_length=1, max_length=20, example='身份证'),
                   # teacher_employer: str = Query(None, title="工作单位", description="工作单位", min_length=1, max_length=20, example='xx学校'),
                   # teacher_highest_education: str = Query(None, title="最高学历", description="最高学历", min_length=1, max_length=20, example='本科'),
                   #   teacher_political_status: str = Query(None, title="政治面貌", description="政治面貌", min_length=1, max_length=20, example='党员'),
                   #      teacher_in_post: str = Query(None, title="在职状态", description="在职状态", min_length=1, max_length=20, example='是'),
                   #      teacher_employment_form: str = Query(None, title="用工形式", description="用工形式", min_length=1, max_length=20, example='合同'),
                   #      teacher_enter_school_time: str = Query(None, title="入校时间", description="入校时间", min_length=1, max_length=20, example='2021-10-10'),
                   #      teacher_approval_status: str = Query(None, title="审批状态", description="审批状态", min_length=1, max_length=20, example='通过')
                   ):
        """
        分页查询
        """
        paging_result = await self.teacher_info_rule.query_teacher_with_page(page_request, condition)
        # teacher_name,teacher_gender,teacher_id_number,teacher_employer,teacher_highest_education,teacher_political_status,teacher_in_post,teacher_employment_form,teacher_enter_school_time,teacher_approval_status)
        return paging_result

    # 新教职工基本信息的功能
    # 新增教职工基本信息
    async def post_newteacherinfo(self, teacher_info: TeacherInfo):
        print(teacher_info)
        res = await self.teacher_info_rule.add_teachers_info(teacher_info)
        return res

    # 获取教职工基本信息
    async def get_newteacherinfo(self, id: str = Query(None, title="教师名称", description="教师名称", min_length=1,
                                                       max_length=20,
                                                       example='张三')):
        res = await self.teacher_info_rule.get_teachers_info_by_id(id)
        return res

    # 编辑教职工基本信息
    async def put_newteacherinfo(self, teacher_info: TeacherInfo):
        res = await self.teacher_info_rule.update_teachers_info(teacher_info)

        return res

    # 删除教职工基本信息
    async def delete_newteacherinfo(self,
                                    id: str = Query(..., title="教师编号", description="教师编号", min_length=1,
                                                    max_length=20, example='123456')):
        res = await self.teacher_info_rule.soft_delete_teachers_info(id)
        return res
