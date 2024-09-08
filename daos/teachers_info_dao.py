from datetime import datetime

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy import select, func, update

from daos.school_dao import SchoolDAO
from daos.tenant_dao import TenantDAO
from models.school import School
from models.teacher_entry_approval import TeacherEntryApproval
from models.teachers import Teacher
from models.teachers_info import TeacherInfo
from views.models.extend_params import ExtendParams
from views.models.school_and_teacher_sync import SupervisorSyncQueryModel
from views.models.system import UnitType
from views.models.teachers import CurrentTeacherQuery, NewTeacher


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

    async def update_teachers_info(self, teachers_info, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teachers_info, *args)
        query = update(TeacherInfo).where(TeacherInfo.teacher_base_id == teachers_info.teacher_base_id).values(
            **update_contents)
        return await self.update(session, query, teachers_info, update_contents, is_commit=is_commit)

    async def delete_teachers_info(self, teachers_info: TeacherInfo):
        session = self.master_db()
        return await self.delete(session, teachers_info)

    # 获取单个教师基本信息
    async def get_teachers_info_by_id(self, teacher_base_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherInfo).join(Teacher, Teacher.teacher_id == TeacherInfo.teacher_id).where(
                TeacherInfo.teacher_base_id == teacher_base_id))
        return result.scalar_one_or_none()

    async def get_teachers_info_by_teacher_id(self, teacher_id):
        session = await self.slave_db()
        result = await session.execute(
            select(TeacherInfo).join(Teacher, Teacher.teacher_id == TeacherInfo.teacher_id).where(
                TeacherInfo.teacher_id == teacher_id))
        return result.scalar_one_or_none()

    async def get_sync_teacher_by_school_no(self, school_no):
        session = await self.slave_db()
        # latest_degree_subquery = (
        #     select(TeacherLearnExperience.institution_of_degree_obtained, TeacherLearnExperience.teacher_id).join(
        #         Teacher,
        #         TeacherLearnExperience.teacher_id == Teacher.teacher_id).where(
        #         TeacherLearnExperience.teacher_id == Teacher.teacher_id, TeacherLearnExperience.is_deleted == False,
        #     ).order_by(
        #         TeacherLearnExperience.degree_award_date.desc()).limit(1).subquery())
        query = select(School.school_no, Teacher.teacher_name, Teacher.teacher_gender, Teacher.teacher_date_of_birth,
                       func.coalesce(TeacherInfo.teacher_number, "").label("teacher_number"),
                       func.coalesce(TeacherInfo.political_status, "").label("political_status"),
                       func.coalesce(TeacherInfo.institution_of_highest_education, "").label(
                           "institution_of_highest_education")).outerjoin(TeacherInfo,
                                                                          Teacher.teacher_id == TeacherInfo.teacher_id,
                                                                          ).join(School,
                                                                                 Teacher.teacher_employer == School.id,
                                                                                 ).where(
            Teacher.teacher_main_status == "employed", Teacher.teacher_sub_status == "active",
            Teacher.is_deleted == False, Teacher.is_approval == False, School.school_no == school_no,
            School.status == "normal").order_by(
            Teacher.teacher_id.desc())
        result = await session.execute(query)
        return result.all()

    async def query_teacher_with_page(self, query_model: NewTeacher, page_request: PageRequest) -> Paging:
        """
        新增教职工分页查询
        教师姓名：teacher_name
        # 教师ID：teacher_id
        身份证号：id_number
        性别：gender
        任职单位：employer
        # 最高学历：highest_education
        政治面貌：political_status
        是否在编：in_post
        用人形式：employment_form
        进本校时间：enter_school_time
        """
        specific_date = datetime.now().date()
        query = select(Teacher.teacher_id,
                       func.coalesce(TeacherInfo.teacher_base_id, 0).label('teacher_base_id'),
                       func.coalesce(TeacherInfo.highest_education, '').label('highest_education'),
                       func.coalesce(TeacherInfo.political_status, '').label('political_status'),
                       func.coalesce(TeacherInfo.in_post, False).label('in_post'),
                       func.coalesce(TeacherInfo.employment_form, '').label('employment_form'),
                       func.coalesce(TeacherInfo.enter_school_time, None).label('enter_school_time'),
                       Teacher.teacher_name, Teacher.teacher_id_number,
                       Teacher.teacher_gender,
                       Teacher.teacher_employer, Teacher.teacher_main_status, Teacher.teacher_sub_status,
                       TeacherEntryApproval.approval_status,
                       School.school_name,
                       ).outerjoin(TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id,
                                   ).outerjoin(School, Teacher.teacher_employer == School.id,
                                               ).where(Teacher.teacher_main_status == "unemployed")

        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender)
        if query_model.teacher_employer:
            if query_model.teacher_employer != 0:
                query = query.where(Teacher.teacher_employer == query_model.teacher_employer)
            else:
                pass
        if query_model.highest_education:
            query = query.where(TeacherInfo.highest_education == query_model.highest_education)
        if query_model.political_status:
            query = query.where(TeacherInfo.political_status == query_model.political_status)
        if query_model.in_post:
            query = query.where(TeacherInfo.in_post == query_model.in_post)
        if query_model.employment_form:
            query = query.where(TeacherInfo.employment_form == query_model.employment_form)
        if query_model.enter_school_time_s and query_model.enter_school_time_e:
            query = query.where(TeacherInfo.enter_school_time.between(query_model.enter_school_time_s,
                                                                      query_model.enter_school_time_e))
        if query_model.teacher_main_status:
            query = query.where(Teacher.teacher_main_status == query_model.teacher_main_status)
        query = query.order_by(Teacher.teacher_id.desc())
        paging = await self.query_page(query, page_request)
        return paging

    async def query_current_teacher_with_page(self, query_model: CurrentTeacherQuery,
                                              page_request: PageRequest,
                                              extend_params: ExtendParams = None) -> Paging:
        """
        新增教职工分页查询
        教师姓名：teacher_name
        # 教师ID：teacher_id
        身份证号：id_number
        性别：gender
        任职单位：employer
        # 最高学历：highest_education
        政治面貌：political_status
        是否在编：in_post
        用人形式：employment_form
        进本校时间：enter_school_time
        """
        query = select(Teacher.teacher_id, TeacherInfo.teacher_base_id, Teacher.teacher_name,
                       Teacher.teacher_id_number,
                       Teacher.teacher_gender, Teacher.teacher_main_status, Teacher.teacher_sub_status,
                       Teacher.teacher_employer, TeacherInfo.highest_education,
                       TeacherInfo.political_status, TeacherInfo.in_post, TeacherInfo.employment_form,
                       School.school_name,
                       TeacherInfo.enter_school_time, Teacher.is_approval).join(TeacherInfo,
                                                                                Teacher.teacher_id == TeacherInfo.teacher_id,
                                                                                ).join(School,
                                                                                       Teacher.teacher_employer == School.id,
                                                                                       ).where(
            Teacher.teacher_main_status == "employed", Teacher.is_deleted == False)
        if extend_params.tenant:
            # 读取类型  读取ID  加到条件里
            tenant_dao = get_injector(TenantDAO)
            school_dao = get_injector(SchoolDAO)
            tenant = await  tenant_dao.get_tenant_by_code(extend_params.tenant.code)
            if tenant.tenant_type == "school":
                school = await school_dao.get_school_by_id(tenant.origin_id)
                if school.institution_category == "institution":
                    query = query.where(School.borough == school.borough)
                else:
                    query = query.where(Teacher.teacher_employer == school.id)
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender)
        if query_model.teacher_employer:
            if query_model.teacher_employer != 0:
                query = query.where(Teacher.teacher_employer == query_model.teacher_employer)
            else:
                pass
        if query_model.highest_education:
            query = query.where(TeacherInfo.highest_education == query_model.highest_education)
        if query_model.political_status:
            query = query.where(TeacherInfo.political_status == query_model.political_status)
        if query_model.in_post:
            query = query.where(TeacherInfo.in_post == query_model.in_post)
        if query_model.employment_form:
            query = query.where(TeacherInfo.employment_form == query_model.employment_form)
        if query_model.enter_school_time_s and query_model.enter_school_time_e:
            query = query.where(TeacherInfo.enter_school_time.between(query_model.enter_school_time_s,
                                                                      query_model.enter_school_time_e))
        query = query.order_by(Teacher.teacher_id.desc())
        paging = await self.query_page(query, page_request)
        return paging
        # 获取所有教师基本信息

    async def get_all_teachers_info(self):
        session = await self.slave_db()
        result = await session.execute(select(TeacherInfo))
        return result.scalars().all()

        # 获取教师基本信息总数

    async def get_teachers_info_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherInfo))
        return result.scalar()

    async def get_teacher_approval(self, teacher_id):
        session = await self.slave_db()
        result = await session.execute(
            select(Teacher.teacher_id, Teacher.teacher_name,
                   TeacherInfo.teacher_base_id,
                   TeacherInfo.ethnicity, TeacherInfo.nationality, TeacherInfo.political_status,
                   TeacherInfo.native_place, TeacherInfo.birth_place, TeacherInfo.former_name,
                   TeacherInfo.marital_status, TeacherInfo.health_condition,
                   TeacherInfo.highest_education, TeacherInfo.institution_of_highest_education,
                   TeacherInfo.special_education_start_time, TeacherInfo.start_working_date,
                   TeacherInfo.enter_school_time, TeacherInfo.source_of_staff,
                   TeacherInfo.staff_category, TeacherInfo.in_post, TeacherInfo.employment_form,
                   TeacherInfo.contract_signing_status, TeacherInfo.current_post_type,
                   TeacherInfo.current_post_level, TeacherInfo.current_technical_position,
                   TeacherInfo.full_time_special_education_major_graduate,
                   TeacherInfo.received_preschool_education_training,
                   TeacherInfo.full_time_normal_major_graduate,
                   TeacherInfo.received_special_education_training,
                   TeacherInfo.has_special_education_certificate,
                   TeacherInfo.information_technology_application_ability,
                   TeacherInfo.free_normal_college_student,
                   TeacherInfo.participated_in_basic_service_project,
                   TeacherInfo.basic_service_start_date, TeacherInfo.basic_service_end_date,
                   TeacherInfo.special_education_teacher, TeacherInfo.dual_teacher,
                   TeacherInfo.has_occupational_skill_level_certificate,
                   TeacherInfo.enterprise_work_experience, TeacherInfo.county_level_backbone,
                   TeacherInfo.psychological_health_education_teacher, TeacherInfo.recruitment_method,
                   TeacherInfo.teacher_number, TeacherInfo.department,
                   TeacherInfo.org_id, TeacherInfo.hmotf, TeacherInfo.hukou_type,
                   TeacherInfo.main_teaching_level, TeacherInfo.teacher_qualification_cert_num,
                   TeacherInfo.teaching_discipline, TeacherInfo.language,
                   TeacherInfo.language_proficiency_level, TeacherInfo.language_certificate_name,
                   TeacherInfo.contact_address, TeacherInfo.contact_address_details,
                   TeacherInfo.email, TeacherInfo.highest_education_level,
                   TeacherInfo.highest_degree_name, TeacherInfo.is_major_graduate,
                   TeacherInfo.other_contact_address_details,
                   Teacher.teacher_gender, Teacher.teacher_id_type, Teacher.teacher_id_number,
                   Teacher.teacher_date_of_birth, Teacher.teacher_employer, Teacher.teacher_avatar,
                   Teacher.teacher_sub_status, Teacher.teacher_main_status, Teacher.identity, Teacher.mobile,
                   School.school_name, Teacher.identity, Teacher.identity_type, School.borough).join(School,
                                                                                                     Teacher.teacher_employer == School.id,
                                                                                                     ).join(
                TeacherInfo,
                Teacher.teacher_id == TeacherInfo.teacher_id,
            ).where(
                Teacher.teacher_id == teacher_id))
        result = result.first()

        # select(Teacher, TeacherInfo.teacher_base_id, TeacherInfo.highest_education,
        #        TeacherInfo.political_status, TeacherInfo.in_post, TeacherInfo.employment_form,
        #        School.school_name,
        #        TeacherInfo.enter_school_time).join(School, Teacher.teacher_employer == School.id,
        #                                            ).join(TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id,
        #                                                   isouter=True,
        #                                                   ).where(Teacher.teacher_id == teacher_id))

        # return result.scalar_one_or_none()

        return result

    async def query_sync_teacher_with_page(self, query_model: SupervisorSyncQueryModel,
                                           page_request: PageRequest) -> Paging:
        query = select(Teacher.teacher_name, Teacher.teacher_id_type, Teacher.teacher_id_number, Teacher.mobile,
                       Teacher.teacher_gender, func.coalesce(TeacherInfo.current_technical_position, ""),
                       func.coalesce(TeacherInfo.staff_category, ""),
                       School.school_name, School.borough).join(Teacher,
                                                                Teacher.teacher_id == TeacherInfo.teacher_id).join(
            School, School.id == Teacher.teacher_employer).where(
            Teacher.teacher_main_status == "employed", Teacher.is_approval == False,
            Teacher.is_deleted == False)
        if query_model.teacher_name:
            query = query.where(Teacher.teacher_name.like(f"%{query_model.teacher_name}%"))
        if query_model.school_name:
            query = query.where(School.school_name.like(f"%{query_model.school_name}%"))
        if query_model.teacher_id_number:
            query = query.where(Teacher.teacher_id_number == query_model.teacher_id_number)
        if query_model.mobile:
            query = query.where(Teacher.mobile == query_model.mobile)
        if query_model.teacher_id_type:
            query = query.where(Teacher.teacher_id_type == query_model.teacher_id_type)
        if query_model.teacher_gender:
            query = query.where(Teacher.teacher_gender == query_model.teacher_gender)
        paging = await self.query_page(query, page_request)
        return paging

    async def get_sync_teacher(self, teacher_id_number):
        session = await self.slave_db()
        query = select(Teacher.teacher_name, Teacher.teacher_id_type, Teacher.teacher_id_number, Teacher.mobile,
                       Teacher.teacher_gender, func.coalesce(TeacherInfo.current_technical_position, ""),
                       func.coalesce(TeacherInfo.staff_category, ""),
                       School.school_name, School.borough).join(
            Teacher,
            Teacher.teacher_id == TeacherInfo.teacher_id).join(School, School.id == Teacher.teacher_employer).where(
            Teacher.teacher_id_number == teacher_id_number, Teacher.teacher_main_status == "employed",
            Teacher.is_deleted == False)
        result = await session.execute(query)
        return result.first()
