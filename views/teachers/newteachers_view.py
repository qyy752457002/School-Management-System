from mini_framework.web.views import BaseView

from views.models.teachers import NewTeacher, TeacherInfo
from fastapi import Query, Depends


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

    async def page(self, condition: NewTeacher = Depends(NewTeacher), page_request=Depends(PageRequest)):
        """
        分页查询
        """
        paging_result = await self.teacher_info_rule.query_teacher_with_page(page_request, condition)
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
