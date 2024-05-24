from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teacher_borrow_dao import TeacherBorrowDAO
from models.teacher_borrow import TeacherBorrow
from views.models.teacher_extend import TeacherBorrowModel,TeacherBorrowUpdateModel


@dataclass_inject
class TeacherBorrowRule(object):
    teacher_borrow_dao: TeacherBorrowDAO

    async def get_teacher_borrow_by_teacher_borrow_id(self, teacher_borrow_id):
        teacher_borrow_db = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowModel)
        return teacher_borrow
    async def add_teacher_borrow(self, teacher_borrow:TeacherBorrowModel):
        teacher_borrow_db = view_model_to_orm_model(teacher_borrow, TeacherBorrow)
        teacher_borrow_db = await self.teacher_borrow_dao.add_teacher_borrow(teacher_borrow_db)
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowModel)
        return teacher_borrow
    async def delete_teacher_borrow(self, teacher_borrow_id):
        exists_teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not exists_teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow_db = await self.teacher_borrow_dao.delete_teacher_borrow(exists_teacher_borrow)
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowModel, exclude=[""])
        return teacher_borrow
    async def update_teacher_borrow(self, teacher_borrow:TeacherBorrowUpdateModel):
        exists_teacher_borrow_info = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow.teacher_borrow_id)
        if not exists_teacher_borrow_info:
            raise Exception(f"编号为{teacher_borrow.teacher_borrow_id}的teacher_borrow不存在")
        need_update_list = []
        for key, value in teacher_borrow.dict().items():
            if value:
                need_update_list.append(key)
        teacher_borrow = await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, *need_update_list)
        return teacher_borrow
    async def get_all_teacher_borrow(self, teacher_id):
          teacher_borrow_db = await self.teacher_borrow_dao.get_all_teacher_borrow(teacher_id)
#          teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowModel, exclude=[""])
          teacher_borrow=[]
          for item in teacher_borrow_db:
              teacher_borrow.append(orm_model_to_view_model(item, TeacherBorrowModel))
          return teacher_borrow_db
