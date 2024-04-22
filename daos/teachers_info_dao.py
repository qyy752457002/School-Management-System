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


    async def update_teachers_info(self, teachers_info: TeacherInfo, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(teachers_info, *args)
        query = update(TeacherInfo).where(TeacherInfo.teacher_id == teachers_info.teacher_id).values(**update_contents)
        return await self.update(session, query, teachers_info, update_contents, is_commit=is_commit)


    async def delete_teachers_info(self, teachers_info: TeacherInfo):
        session = self.master_db()
        return await self.delete(session, teachers_info)

    # 获取单个教师基本信息
    async def get_teachers_info_by_id(self, teachers_info_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherInfo).where(TeacherInfo.teacher_id == teachers_info_id))
        return result.scalar_one_or_none()

    # async def get_teachers_info_by_username(self, username):
    #     session = await self.slave_db()
    #     result = await session.execute(select(TeacherInfo).where(TeacherInfo.username) == username)
    #     return result.scalar_one_or_none()

    async def query_teacher_with_page(self, page_request: PageRequest, condition) -> Paging:
        """
        新增教职工分页查询
        """
        query = select(Teacher.teacher_name, Teacher.teacher_id_number, Teacher.teacher_gender,
                       Teacher.teacher_employer, Teacher.teacher_approval_status, TeacherInfo.highest_education,
                       TeacherInfo.political_status, TeacherInfo.in_post, TeacherInfo.employment_form,
                       TeacherInfo.enter_school_time).join(TeacherInfo, Teacher.teacher_id == TeacherInfo.teacher_id)
        properties = vars(condition)
        print(f'properties{properties}')
        conditions = []
        for key, value in properties.items():
            if hasattr(Teacher, key):
                query = query.where(getattr(Teacher, key) == value)
            if hasattr(TeacherInfo, key):
                query = query.where(getattr(Teacher, key) == value)

        if conditions:
            query = query.where(*conditions)
        else:
            query = query
        print(query)
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