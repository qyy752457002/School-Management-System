from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.teachers_info import TeacherInfo
from models.teachers import Teacher
from views.models.teachers import TeacherInfo as TeacherInfoModel


class TeachersInfoDao(DAOBase):
    # 新增教师基本信息
    async def add_teachers_info(self, teachers_info):
        """
        传入的参数
        """
        session = await self.master_db()
        session.add(teachers_info)
        await session.commit()
        await session.refresh(teachers_info)
        return teachers_info

    # 编辑教师基本信息
    # async def update_teachers_info(self, teachers_info: TeacherInfoModel):
    #     session = await self.master_db()
    #     update_stmt = update(TeacherInfo).where(TeacherInfo.id == teachers_info.id).values(
    #         nationality=teachers_info.nationality,
    #         ethnicity=teachers_info.ethnicity,
    #         political_status=teachers_info.political_status,
    #         native_place=teachers_info.native_place,
    #         birth_place=teachers_info.birth_place,
    #         former_name=teachers_info.former_name,
    #         marital_status=teachers_info.marital_status,
    #         health_condition=teachers_info.health_condition,
    #         highest_education=teachers_info.highest_education,
    #         institution_of_highest_education=teachers_info.institution_of_highest_education,
    #         special_education_start_time=teachers_info.special_education_start_time,
    #         start_working_date=teachers_info.start_working_date,
    #         enter_school_time=teachers_info.enter_school_time,
    #         source_of_staff=teachers_info.source_of_staff,
    #         staff_category=teachers_info.staff_category,
    #         in_post=teachers_info.in_post,
    #         employment_form=teachers_info.employment_form,
    #         contract_signing_status=teachers_info.contract_signing_status,
    #         current_post_type=teachers_info.current_post_type,
    #         current_post_level=teachers_info.current_post_level,
    #         current_technical_position=teachers_info.current_technical_position,
    #         full_time_special_education_major_graduate=teachers_info.full_time_special_education_major_graduate,
    #         received_preschool_education_training=teachers_info.received_preschool_education_training,
    #         full_time_normal_major_graduate=teachers_info.full_time_normal_major_graduate,
    #         received_special_education_training=teachers_info.received_special_education_training,
    #         has_special_education_certificate=teachers_info.has_special_education_certificate,
    #         information_technology_application_ability=teachers_info.information_technology_application_ability,
    #         free_normal_college_student=teachers_info.free_normal_college_student,
    #         participated_in_basic_service_project=teachers_info.participated_in_basic_service_project,
    #         basic_service_start_date=teachers_info.basic_service_start_date,
    #         basic_service_end_date=teachers_info.basic_service_end_date,
    #         special_education_teacher=teachers_info.special_education_teacher,
    #         dual_teacher=teachers_info.dual_teacher,
    #         has_occupational_skill_level_certificate=teachers_info.has_occupational_skill_level_certificate,
    #         enterprise_work_experience=teachers_info.enterprise_work_experience,
    #         county_level_backbone=teachers_info.county_level_backbone,
    #         psychological_health_education_teacher=teachers_info.psychological_health_education_teacher,
    #         recruitment_method=teachers_info.recruitment_method,
    #         teacher_number=teachers_info.teacher_number
    #     )
    #     await session.execute(update_stmt)
    #     await session.commit()
    #     return teachers_info

    async def update_teachers_info(self, teachers_info: TeacherInfo, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teachers_info, *args)
        query = update(Teacher).where(Teacher.id == teachers_info.id).values(**update_contents)
        return await self.update(session, query, teachers_info, update_contents, is_commit=is_commit)

    # 删除教师基本信息
    async def delete_teachers_info(self, teachers_info: TeacherInfo):
        session = self.master_db()
        return await self.delete(session, teachers_info)

    # 获取单个教师基本信息
    async def get_teachers_info_by_id(self, teachers_info_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherInfo).where(TeacherInfo.id == teachers_info_id))
        return result.scalar_one_or_none()

    # async def get_teachers_info_by_name(self, teachers_name):
    #     session = await self.slave_db()
    #     result = await session.execute(select(TeacherInfo).where(Teacher.teachers_name) == teachers_name)
    #     return result.scalar_one_or_none()

    # 尝试联合多表分页查询
    async def query_teacher_with_page(self, page_request: PageRequest, condition) -> Paging:
        query = select(Teacher.teacher_name, Teacher.teacher_id_number, Teacher.teacher_gender,
                       Teacher.teacher_employer, Teacher.teacher_approval_status, TeacherInfo.highest_education,
                       TeacherInfo.political_status, TeacherInfo.in_post, TeacherInfo.employment_form,
                       TeacherInfo.enter_school_time).select_from(
            Teacher.join(TeacherInfo, Teacher.id == TeacherInfo.teacher_number)
        )
        properties = vars(condition)
        conditions = []
        for key, value in properties.items():
            if hasattr(Teacher, key):
                conditions.append(getattr(Teacher, key) == value)
            if hasattr(TeacherInfo, key):
                conditions.append(getattr(TeacherInfo, key) == value)
        if conditions:
            query = query.where(*conditions)
        paging = await self.query_page(query, page_request)
        return paging
