from datetime import date, datetime

from sqlalchemy import select, func, update

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.school import School
from models.teachers_info import TeacherInfo
from models.teachers import Teacher
from views.models.teachers import CurrentTeacherQuery, NewTeacher, TeacherApprovalQuery
from models.teacher_entry_approval import TeacherEntryApproval


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
        if query_model.enter_school_time:
            query = query.where(TeacherInfo.enter_school_time == query_model.enter_school_time)
        if query_model.teacher_main_status:
            query = query.where(Teacher.teacher_main_status == query_model.teacher_main_status)
        query = query.order_by(Teacher.teacher_id.desc())
        paging = await self.query_page(query, page_request)
        return paging

    async def query_current_teacher_with_page(self, query_model: CurrentTeacherQuery,
                                              page_request: PageRequest) -> Paging:
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
        query = select(Teacher.teacher_id, TeacherInfo.teacher_base_id, Teacher.teacher_name, Teacher.teacher_id_number,
                       Teacher.teacher_gender,
                       Teacher.teacher_employer, TeacherInfo.highest_education,
                       TeacherInfo.political_status, TeacherInfo.in_post, TeacherInfo.employment_form,
                       School.school_name,
                       TeacherInfo.enter_school_time).join(TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id,
                                                           ).join(School, Teacher.teacher_employer == School.id,
                                                                  ).where(Teacher.teacher_main_status == "employed")

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
        if query_model.enter_school_time:
            query = query.where(TeacherInfo.enter_school_time == query_model.enter_school_time)
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
