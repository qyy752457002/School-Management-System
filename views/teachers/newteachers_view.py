from mini_framework.web.views import BaseView

from views.models.teachers import Teachers, NewTeacher, TeacherInfo
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse


class NewTeachersView(BaseView):

    # 新增教职工登记
    async def post_newteacher(self, teachers: Teachers):
        print(teachers)
        return teachers

    # 分页查询
    async def page(self, new_teacher: NewTeacher, page_request=Depends(PageRequest)):
        print(page_request)
        items = []

        res = NewTeacher(
            name="张三",
            id_number="123456789",
            gender="男",
            employer="xx学校",
            highest_education="本科",
            political_status="党员",
            in_post="是",
            employment_form="合同",
            enter_school_time="2021-10-10",
            approval_status="通过"
        )

        for i in range(0, page_request.per_page):
            items.append(res)

        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10,
                                 per_page=page_request.per_page, total=100, items=items)

    # 新教职工基本信息的功能
    # 新增教职工基本信息
    async def post_newteacherinfo(self, teacher_info: TeacherInfo):
        print(teacher_info)
        return teacher_info

    # 获取教职工基本信息
    async def get_newteacherinfo(self, name: str = Query(None, title="教师名称", description="教师名称", min_length=1, max_length=20,
                                          example='张三')):
        res = TeacherInfo(
            name=name,
            teacher_id="123456",
            nationality="中国",
            ethnic="汉族",
            political_status="党员",
            native_place="沈阳",
            birth_place="沈阳",
            former_name="张三",
            marital_status="已婚",
            health_condition="良好",
            highest_education="本科",
            institution_of_highest_education="沈阳师范大学",
            special_education_start_time="2021-10-10",
            start_working_date="2010-01-01",
            enter_school_time="2010-01-01",
            source_of_staff="招聘",
            staff_category="教师",
            in_post="是",
            employment_form="合同",
            contract_signing_status="已签",
            current_post_type="教师",
            current_post_level="5",
            current_technical_position="教师",
            full_time_special_education_major_graduate="是",
            received_preschool_education_training="是",
            full_time_normal_major_graduate="是",
            received_special_education_training="是",
            has_special_education_certificate="是",
            information_technology_application_ability="良好",
            free_normal_college_student="是",
            participated_in_basic_service_project="是",
            basic_service_start_date="2021-10-10",
            basic_service_end_date="2021-10-10",
            special_education_teacher="是",
            dual_teacher="是",
            has_occupational_skill_level_certificate="是",
            enterprise_work_experience="5",
            county_level_backbone="是",
            psychological_health_education_teacher="是",
            recruitment_method="招聘",
            teacher_number="123456"
        )

        return res

    # 编辑教职工基本信息
    async def put_newteacherinfo(self, teacher_info: TeacherInfo):
        print(teacher_info)
        return teacher_info

    # 删除教职工基本信息
    async def delete_newteacherinfo(self,
                                 teacher_id: str = Query(..., title="教师编号", description="教师编号", min_length=1,
                                                         max_length=20, example='123456')):
        print(teacher_id)
        return teacher_id
