from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers_info import TeacherInfo
from views.models.teachers import TeacherInfo as TeachersInfoModel
from sqlalchemy import select, func, update


@dataclass_inject
class TeachersInfoRule(object):
    teachers_info_dao: TeachersInfoDao

    # 查询单个教职工基本信息
    async def get_teachers_info_by_id(self, teachers_info_id):
        teachers_info_db = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info_id)
        # 可选 ,
        teachers_info = orm_model_to_view_model(teachers_info_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    # 添加单个教职工基本信息
    # async def add_teachers_info(self, teachers_info: TeachersInfoModel):
    # exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info.id)
    # if exists_teachers_info:
    #     raise Exception(f"编号为{teachers_info.id}教师已存在")
    # teachers_info_db = TeacherInfo()
    # teachers_info_db.nationality = teachers_info.nationality
    # teachers_info_db.ethnicity = teachers_info.ethnicity
    # teachers_info_db.political_status = teachers_info.political_status
    # teachers_info_db.native_place = teachers_info.native_place
    # teachers_info_db.birth_place = teachers_info.birth_place
    # teachers_info_db.former_name = teachers_info.former_name
    # teachers_info_db.marital_status = teachers_info.marital_status
    # teachers_info_db.health_condition = teachers_info.health_condition
    # teachers_info_db.highest_education = teachers_info.highest_education
    # teachers_info_db.institution_of_highest_education = teachers_info.institution_of_highest_education
    # teachers_info_db.special_education_start_time = teachers_info.special_education_start_time
    # teachers_info_db.start_working_date = teachers_info.start_working_date
    # teachers_info_db.enter_school_time = teachers_info.enter_school_time
    # teachers_info_db.source_of_staff = teachers_info.source_of_staff
    # teachers_info_db.staff_category = teachers_info.staff_category
    # teachers_info_db.in_post = teachers_info.in_post
    # teachers_info_db.employment_form = teachers_info.employment_form
    # teachers_info_db.contract_signing_status = teachers_info.contract_signing_status
    # teachers_info_db.current_post_type = teachers_info.current_post_type
    # teachers_info_db.current_post_level = teachers_info.current_post_level
    # teachers_info_db.current_technical_position = teachers_info.current_technical_position
    # teachers_info_db.full_time_special_education_major_graduate = teachers_info.full_time_special_education_major_graduate
    # teachers_info_db.received_preschool_education_training = teachers_info.received_preschool_education_training
    # teachers_info_db.full_time_normal_major_graduate = teachers_info.full_time_normal_major_graduate
    # teachers_info_db.received_special_education_training = teachers_info.received_special_education_training
    # teachers_info_db.has_special_education_certificate = teachers_info.has_special_education_certificate
    # teachers_info_db.information_technology_application_ability = teachers_info.information_technology_application_ability
    # teachers_info_db.free_normal_college_student = teachers_info.free_normal_college_student
    # teachers_info_db.participated_in_basic_service_project = teachers_info.participated_in_basic_service_project
    # teachers_info_db.basic_service_start_date = teachers_info.basic_service_start_date
    # teachers_info_db.basic_service_end_date = teachers_info.basic_service_end_date
    # teachers_info_db.special_education_teacher = teachers_info.special_education_teacher
    # teachers_info_db.dual_teacher = teachers_info.dual_teacher
    # teachers_info_db.has_occupational_skill_level_certificate = teachers_info.has_occupational_skill_level_certificate
    # teachers_info_db.enterprise_work_experience = teachers_info.enterprise_work_experience
    # teachers_info_db.county_level_backbone = teachers_info.county_level_backbone
    # teachers_info_db.psychological_health_education_teacher = teachers_info.psychological_health_education_teacher
    # teachers_info_db.recruitment_method = teachers_info.recruitment_method
    # teachers_info_db.teacher_number = teachers_info.teacher_number
    #
    # teachers_info_db = await self.teachers_info_dao.add_teachers_info(teachers_info_db)
    # teachers_info = orm_model_to_view_model(teachers_info_db, TeachersInfoModel)
    # return teachers_info
    async def add_teachers_info(self, teachers_info: TeachersInfoModel):
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=[" "])
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def update_teachers_info(self, teachers_info):
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info.teacher_id)
        if not exists_teachers_info:
            raise Exception(f"编号为{teachers_info.id}教师不存在")
        need_update_list = []
        for key, value in teachers_info.dict().items():
            if value:
                need_update_list.append(key)
        teachers_info = await self.teachers_info_dao.update_teachers_info(teachers_info, *need_update_list)
        return teachers_info

    # 删除单个教职工基本信息
    async def delete_teachers_info(self, teachers_info_id):
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info_id)
        if not exists_teachers_info:
            raise Exception(f"编号为{teachers_info_id}教师不存在")
        teachers_info_db = await self.teachers_info_dao.delete_teachers_info(exists_teachers_info)
        return teachers_info_db

    # 分页查询
    async def query_teacher_with_page(self, page_request: PageRequest, condition):
        """
        分页查询
        """
        paging = await self.teachers_info_dao.query_teacher_with_page(page_request, condition)
        paging_result = PaginatedResponse.from_paging(paging, TeachersInfoModel)
        return paging_result
