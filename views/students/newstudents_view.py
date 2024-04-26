from typing import List

from mini_framework.web.views import BaseView

from views.models.students import NewStudents, NewStudentsQuery, NewStudentsQueryRe, StudentsKeyinfo, StudentsBaseInfo, \
    StudentsFamilyInfo
# from fastapi import Field
from mini_framework.web.views import BaseView

from views.models.teachers import NewTeacher, TeacherInfo
from fastapi import Query, Depends

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from models.students import Student
from rules.students_rule import StudentsRule
from rules.students_base_info_rule import StudentsBaseInfoRule
from views.models.students import StudentsKeyinfo as StudentsKeyinfoModel
from views.models.students import NewStudents, NewBaseInfoCreate,NewBaseInfoUpdate,StudentsFamilyInfoCreate
from views.models.students import NewStudentsFlowOut,StudentsUpdateFamilyInfo
from datetime import date
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_family_info_rule import StudentsFamilyInfoRule


class NewsStudentsView(BaseView):
    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)

    async def post_newstudent(self, students: NewStudents):
        """
        新增新生信息
        """
        res = await self.students_rule.add_students(students)
        students.student_id =  res.student_id
        vm2 = NewBaseInfoCreate(student_id=students.student_id,school_id=students.school_id )
        # vm2.student_id = students.student_id

        res2 = await self.students_base_info_rule.add_students_base_info(vm2)

        return res

    # 分页查询
    #
    async def page_newstudent(self, new_students_query=Depends(NewStudentsQuery),
                              page_request=Depends(PageRequest)):
        """
        分页查询
        """
        paging_result = await self.students_base_info_rule.query_students_base_info_with_page(new_students_query,
                                                                                              page_request)
        return paging_result

    async def get_newstudentkeyinfo(self, student_id: str = Query(..., title="学生编号", description="学生编号",
                                                                  example="SC2032633")):
        """新生查询关键信息"""
        res = await self.students_rule.get_students_by_id(student_id)
        return res

    async def put_newstudentkeyinfo(self, new_students_key_info: StudentsKeyinfo):
        """"
        新生编辑关键信息
        """
        print(new_students_key_info)
        res = await self.students_rule.update_students(new_students_key_info)
        return res

    async def delete_newstudentkeyinfo(self, student_id: str = Query(..., title="学生编号", description="学生编号", )):
        """
        删除新生关键信息
        """
        await self.students_rule.delete_students(student_id)
        return str(student_id)

    async def patch_newstudent_flowout(self, new_students_flow_out: NewStudentsFlowOut):
        """
        新生流出
        """
        res_base_info = await self.students_base_info_rule.update_students_base_info(
            new_students_flow_out)  # 修改基本信息中的流出时间等
        return res_base_info

    # todo 仅仅修改一个状态就行

    async def patch_formaladmission(self, student_id: List[str] = Query(..., description="学生id", min_length=1,
                                                                        max_length=20, example=["SC2032633"]),
                                    ):
        print(student_id)
        return student_id


class NewsStudentsInfoView(BaseView):
    """
    新生基本信息
    """

    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)

    async def get_newstudentbaseinfo(self, student_id: str = Query(..., title="学生编号", description="学生编号",
                                                                   example="SC2032633")):
        """
        查询新生基本信息
        """
        res = await self.students_base_info_rule.get_students_base_info_by_student_id(student_id)
        return res

    async def post_newstudentbaseinfo(self, new_students_base_info: NewBaseInfoCreate):
        """
        新生新增基本信息
        """
        res = await self.students_base_info_rule.add_students_base_info(new_students_base_info)
        return res

    async def put_newstudentbaseinfo(self, new_students_base_info: NewBaseInfoUpdate):
        """
        新生编辑基本信息
        """
        res = await self.students_base_info_rule.update_students_base_info(new_students_base_info)
        return res


    async def patch_newstudent_classdivision(self,
                                             class_id: int  = Query(..., title="", description="班级ID",),
                                             student_id:  str  = Query(..., title="", description="学生ID/逗号分割",),

                                             ):
        """
        分班
        """
        res = await self.students_base_info_rule.update_students_class_division(class_id, student_id)
        return res

    async def delete_newstudentbaseinfo(self,
                                        student_id: str = Query(..., title="学生编号", description="学生编号", )):
        """
        新生删除基本信息
        """
        await self.students_base_info_rule.delete_students_base_info(student_id)
        return str(student_id)


class NewsStudentsFamilyInfoView(BaseView):
    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_family_info_rule=get_injector(StudentsFamilyInfoRule)


    async def post_newstudentfamilyinfo(self, new_students_family_info: StudentsFamilyInfoCreate):
        """
        新生增加家庭信息
        """
        res = await self.students_family_info_rule.add_students_family_info(new_students_family_info)

        return res

    async def put_newstudentfamilyinfo(self, new_students_family_info: StudentsUpdateFamilyInfo):
        """
        新生编辑家庭信息
        """
        res = await self.students_family_info_rule.update_students_family_info(new_students_family_info)
        return res

    async def delete_newstudentfamilyinfo(self,
                                          student_family_info_id: str = Query(..., title="学生编号",
                                                                  description="学生编号", )):
        """
        新生删除家庭信息
        """
        await self.students_family_info_rule.delete_students_family_info(student_family_info_id)
        return str(student_family_info_id)

    async def get_newstudentfamilyinfo(self,
                                       student_family_info_id: str = Query(..., title="学生编号", description="学生编号", )):
        """
        查询单条家庭信息
        """
        res = await self.students_family_info_rule.get_students_family_info_by_id(student_family_info_id)
        return res

    async def get_newstudentfamilyinfoall(self,
                                          student_id: str = Query(..., title="学生编号", description="学生编号", )):
        """
        新生查询家庭信息
        """
        res = await self.students_family_info_rule.get_all_students_family_info(student_id)
        return res
