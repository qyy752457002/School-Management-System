from sqlalchemy import select, func, update,  desc

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.grade import Grade


class GradeDAO(DAOBase):

    async def get_grade_by_id(self, grade_id):
        session = await self.slave_db()
        result = await session.execute(select(Grade).where(Grade.id == int(grade_id)).where(Grade.is_deleted == False))
        return result.scalar_one_or_none()
    async def get_grade_by_id_and_school_id(self, grade_id, school_id, section):
        session = await self.slave_db()
        result = await session.execute(
            select(Grade).where(Grade.id == int(grade_id), Grade.section == section, Grade.school_id == int(school_id),
                                Grade.is_deleted == False))
        return result.scalar_one_or_none()
    async def get_grade_by_index_and_school_id(self, grade_index, school_id, section):
        session = await self.slave_db()
        result = await session.execute(
            select(Grade).where(Grade.grade_index == grade_index, Grade.section == section, Grade.school_id == int(school_id),
                                Grade.is_deleted == False))
        return result.scalar_one_or_none()

    async def get_grade_by_grade_name(self, grade_name, grade=None):
        session = await self.slave_db()
        #  定义  市区的字段 是  编码
        query = select(Grade).where(Grade.grade_name == grade_name).where(Grade.is_deleted == False)
        if grade.school_id:
            query = query.where(Grade.school_id == int(grade.school_id))
        if grade.city:
            query = query.where(Grade.city == grade.city)
        if grade.district:
            query = query.where(Grade.district == grade.district)
        if grade.school_type:
            query = query.where(Grade.school_type == grade.school_type)
        if grade.grade_type:
            query = query.where(Grade.grade_type == grade.grade_type)

        result = await session.execute(query)
        return result.first()

    async def add_grade(self, grade):
        session = await self.master_db()
        session.add(grade)
        await session.commit()
        await session.refresh(grade)
        return grade

    async def update_grade(self, grade):
        session = await self.master_db()
        session.execute(update(Grade).where(Grade.id == grade.id).values())
        await session.commit()
        return grade

    async def update_grade_byargs(self, grade: Grade, *args, is_commit: bool = True):
        grade.id = int(grade.id)
        session = await self.master_db()
        update_contents = get_update_contents(grade, *args)
        query = update(Grade).where(Grade.id == grade.id).values(**update_contents)
        return await self.update(session, query, grade, update_contents, is_commit=is_commit)

    async def softdelete_grade(self, grade):
        grade.id = int(grade.id)

        session = await self.master_db()
        deleted_status = True
        update_stmt = update(Grade).where(Grade.id == grade.id).values(
            is_deleted=deleted_status,
        )
        await session.execute(update_stmt)
        await session.commit()
        return grade

    async def delete_grade(self, grade):
        session = await self.master_db()
        await self.delete(session, grade,True)
        # await session.execute(  delete(Grade).where(Grade.id == grade.id) )
        # await session.commit()
        return grade

    async def get_all_grades(self):
        session = await self.slave_db()
        result = await session.execute(select(Grade))
        return result.scalars().all()

    async def get_grade_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(Grade))
        return result.scalar()

    async def query_grade_with_page(self, grade_name, school_id, page_request: PageRequest, city='',
                                    district='') -> Paging:
        query = select(Grade).where(Grade.is_deleted == False).order_by(desc(Grade.id))
        if grade_name:
            query = query.where(Grade.grade_name.like(f'%{grade_name}%'))
        if school_id:
            query = query.where(Grade.school_id == school_id)
        if city:
            query = query.where(Grade.city == city)
        if district:
            query = query.where(Grade.district == district)
        paging = await self.query_page(query, page_request)
        return paging

    # 根据学校ID和年级ID 设置年级的班级数量自增1
    async def increment_class_number(self, school_id, grade_id):
        grade_id = int(grade_id)
        school_id = int(school_id)

        session = await self.master_db()
        query = update(Grade).where(Grade.school_id == school_id).where(Grade.id == grade_id).values(
            class_number=Grade.class_number + 1
        )
        await session.execute(query)
        await session.commit()
        # await session.refresh()
