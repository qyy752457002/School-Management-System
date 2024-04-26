from sqlalchemy import select, func, update, desc

from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest
from models.student_session import StudentSession


class StudentSessionDao(DAOBase):
    async def add_student_session(self, student_session):
        """
        新增类别
        """
        session = await self.master_db()
        session.add(student_session)
        await session.commit()
        await session.refresh(student_session)
        return student_session

    async def update_student_session(self, student_session: StudentSession, *args, is_commit: bool = True):
        """
        编辑类别
        """
        session = await self.master_db()
        update_contents = get_update_contents(student_session, *args)
        query = update(StudentSession).where(StudentSession.session_id == student_session.session_id).values(**update_contents)
        return await self.update(session, query, student_session, update_contents, is_commit=is_commit)

    async def get_student_session_by_id(self, session_id):
        """
        获取单个类别
        """
        session = await self.slave_db()
        result = await session.execute(select(StudentSession).where(StudentSession.session_id == session_id))
        return result.scalar_one_or_none()

    async def delete_student_session(self, student_session: StudentSession):
        """
        删除单个类别
        """
        session = self.master_db()
        return await self.delete(session, student_session)

    async def get_all_student_sessions(self):
        session = await self.slave_db()
        result = await session.execute(select(StudentSession))
        return result.scalars().all()

    async def get_student_session_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(StudentSession))
        return result.scalar()


    async def query_session_with_page(self, page_request: PageRequest, status ) -> Paging:
        query = select(StudentSession). order_by(desc(StudentSession.session_id))

        if status:
            query = query.where(StudentSession.session_status == status)


        paging = await self.query_page(query, page_request)
        return paging
