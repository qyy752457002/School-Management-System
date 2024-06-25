from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_dao import TeachersDao
from daos.teacher_borrow_dao import TeacherBorrowDAO
from models.teacher_borrow import TeacherBorrow

from business_exceptions.teacher import TeacherNotFoundError
from views.models.teacher_transaction import TeacherTransactionQuery, TeacherTransactionQueryRe, \
    TeacherBorrowReModel, TeacherBorrowGetModel, TeacherBorrowQueryModel, TeacherBorrowQueryReModel


@dataclass_inject
class TeacherBorrowRule(object):
    teacher_borrow_dao: TeacherBorrowDAO
    teachers_dao: TeachersDao

    async def get_teacher_borrow_by_teacher_borrow_id(self, teacher_borrow_id):
        teacher_borrow_db = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not teacher_borrow_db:
            raise TeacherNotFoundError()
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel)
        return teacher_borrow

    async def add_teacher_borrow_in(self, teacher_borrow: TeacherBorrowReModel):
        """
        借入
        """
        # todo 需要增加获取调入流程实例id
        teacher_borrow_db = view_model_to_orm_model(teacher_borrow, TeacherBorrow)
        teacher_borrow_db = await self.teacher_borrow_dao.add_teacher_borrow(teacher_borrow_db)
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel)
        return teacher_borrow

    async def add_teacher_borrow_out(self, teacher_borrow: TeacherBorrowReModel):
        """
        借出
        """
        # todo 需要增加获取调出流程实例id
        teacher_borrow_db = view_model_to_orm_model(teacher_borrow, TeacherBorrow)
        teacher_borrow_db = await self.teacher_borrow_dao.add_teacher_borrow(teacher_borrow_db)
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel)
        return teacher_borrow

    async def delete_teacher_borrow(self, teacher_borrow_id):
        exists_teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not exists_teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow_db = await self.teacher_borrow_dao.delete_teacher_borrow(exists_teacher_borrow)
        teacher_borrow = orm_model_to_view_model(teacher_borrow_db, TeacherBorrowReModel, exclude=[""])
        return teacher_borrow

    async def update_teacher_borrow(self, teacher_borrow: TeacherBorrowReModel):
        exists_teacher_borrow_info = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(
            teacher_borrow.teacher_borrow_id)
        if not exists_teacher_borrow_info:
            raise Exception(f"编号为{teacher_borrow.teacher_borrow_id}的teacher_borrow不存在")
        need_update_list = []
        for key, value in teacher_borrow.dict().items():
            if value:
                need_update_list.append(key)
        teacher_borrow = await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, *need_update_list)
        return teacher_borrow

    async def get_all_teacher_borrow(self, teacher_id):
        """
        详情页查询单个老师所有借动信息
        """
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        teacher_borrow_db = await self.teacher_borrow_dao.get_all_teacher_borrow(teacher_id)
        teacher_borrow = []
        for item in teacher_borrow_db:
            teacher_borrow.append(orm_model_to_view_model(item, TeacherBorrowGetModel))
        return teacher_borrow

    async def query_teacher_borrow(self, teacher_borrow: TeacherTransactionQuery):
        """
        查询老师是否在系统内
        """
        teacher_borrow_db = await self.teachers_dao.query_teacher_transfer(teacher_borrow)
        teacher_borrow_inner = True  # 系统内互转
        if teacher_borrow_db:
            teacher_borrow_db = orm_model_to_view_model(teacher_borrow_db, TeacherTransactionQueryRe)
            return teacher_borrow_db, teacher_borrow_inner
        else:
            teacher_borrow_inner = False
            return teacher_borrow_db, teacher_borrow_inner

    # 借动管理分页查询相关
    async def query_borrow_out_with_page(self, type, query_model: TeacherBorrowQueryModel,
                                           page_request: PageRequest):
        if type == "launch":
            teacher_borrow_db = await self.teacher_borrow_dao.query_borrow_out_launch_with_page(query_model,
                                                                                                         page_request)
        elif type == "approval":
            teacher_borrow_db = await self.teacher_borrow_dao.query_borrow_out_approval_with_page(query_model,
                                                                                                           page_request)
        paging_result = PaginatedResponse.from_paging(teacher_borrow_db, TeacherBorrowQueryReModel)
        return paging_result

    async def query_borrow_in_with_page(self, type, query_model: TeacherBorrowQueryModel,
                                           page_request: PageRequest):
        if type == "launch":
            teacher_borrow_db = await self.teacher_borrow_dao.query_borrow_in_launch_with_page(query_model,
                                                                                                         page_request)
        elif type == "approval":
            teacher_borrow_db = await self.teacher_borrow_dao.query_borrow_in_approval_with_page(query_model,
                                                                                                           page_request)
        paging_result = PaginatedResponse.from_paging(teacher_borrow_db, TeacherBorrowQueryReModel)
        return paging_result


    #借动管理审批相关
    # async def submitting(self, teacher_borrow_id):
    #     teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
    #     if not teacher_borrow:
    #         raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
    #     teacher_borrow.approval_status = "submitting"
    #     return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")
    #
    # async def submitted(self, teacher_borrow_id):
    #     teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
    #     if not teacher_borrow:
    #         raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
    #     teacher_borrow.approval_status = "submitted"
    #     return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")

    async def borrow_approved(self, teacher_borrow_id):
        teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow.approval_status = "approved"
        return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")

    async def borrow_rejected(self, teacher_borrow_id):
        teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow.approval_status = "rejected"
        return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")

    async def borrow_revoked(self, teacher_borrow_id):
        teacher_borrow = await self.teacher_borrow_dao.get_teacher_borrow_by_teacher_borrow_id(teacher_borrow_id)
        if not teacher_borrow:
            raise Exception(f"编号为的{teacher_borrow_id}teacher_borrow不存在")
        teacher_borrow.approval_status = "revoked"
        return await self.teacher_borrow_dao.update_teacher_borrow(teacher_borrow, "approval_status")
