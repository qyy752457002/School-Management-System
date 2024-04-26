from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.student_session_dao import StudentSessionDao
from models.student_session import StudentSession
from views.models.students import StudentSession as StudentSessionModel


@dataclass_inject
class StudentSessionRule(object):
    student_session_dao: StudentSessionDao

    async def get_student_session_by_id(self, session_id):
        """
        获取单个类别
        """
        session_db = await self.student_session_dao.get_student_session_by_id(session_id)
        session = orm_model_to_view_model(session_db, StudentSessionModel, exclude=[""])
        return session

    async def add_student_session(self, session: StudentSession):
        """
        新增类别
        """
        session_db = view_model_to_orm_model(session, StudentSession, exclude=["session_id"])
        session_db = await self.student_session_dao.add_student_session(session_db)
        session = orm_model_to_view_model(session_db, StudentSessionModel, exclude=[""])
        return session

    async def update_student_session(self, session):
        """
        编辑类别
        """
        exists_session = await self.student_session_dao.get_student_session_by_id(session.session_id)
        if not exists_session:
            raise Exception(f"编号为{session.session_id}类别不存在")
        need_update_list = []
        for key, value in session.dict().items():
            if value:
                need_update_list.append(key)
        session = await self.student_session_dao.update_student_session(session, *need_update_list)
        return session

    async def delete_student_session(self, session_id):
        """
        删除类别
        """
        exists_session = await self.student_session_dao.get_student_session_by_id(session_id)
        if not exists_session:
            raise Exception(f"编号为{session_id}类别不存在")
        session_db = await self.student_session_dao.delete_student_session(exists_session)
        return session_db

    async def get_all_student_sessions(self):
        """
        获取所有类别
        """
        session_db = await self.student_session_dao.get_all_student_sessions()
        # session = orm_model_to_view_model(session_db, StudentSessionModel, exclude=[""])
        return session_db

    async def get_student_session_count(self):
        """
        获取类别数量
        """
        count = await self.student_session_dao.get_student_session_count()
        return count
