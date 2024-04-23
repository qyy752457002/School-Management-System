from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.teachers_info_dao import TeachersInfoDao
from models.teachers_info import TeacherInfo
from views.models.teachers import TeacherInfo as TeachersInfoModel
from views.models.teachers import NewTeacher, NewTeacherRe
from sqlalchemy import select, func, update
from business_exceptions.teacher import TeacherNotFoundError, TeacherInfoNotFoundError


@dataclass_inject
class TeachersInfoRule(object):
    teachers_info_dao: TeachersInfoDao

    # 查询单个教职工基本信息
    async def get_teachers_info_by_id(self, teachers_info_id):
        teachers_info_db = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info_id)
        if not teachers_info_db:
            raise TeacherInfoNotFoundError()
        teachers_info = orm_model_to_view_model(teachers_info_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def add_teachers_info(self, teachers_info: TeachersInfoModel):
        teachers_inf_db = view_model_to_orm_model(teachers_info, TeacherInfo, exclude=[" "])
        teachers_inf_db = await self.teachers_info_dao.add_teachers_info(teachers_inf_db)
        teachers_info = orm_model_to_view_model(teachers_inf_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def update_teachers_info(self, teachers_info):
        exists_teachers_info = await self.teachers_info_dao.get_teachers_info_by_id(teachers_info.teacher_id)
        if not exists_teachers_info:
            raise TeacherInfoNotFoundError()
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
            raise TeacherInfoNotFoundError()
        teachers_info_db = await self.teachers_info_dao.delete_teachers_info(exists_teachers_info)
        teachers_info = orm_model_to_view_model(teachers_info_db, TeachersInfoModel, exclude=[""])
        return teachers_info

    async def query_teacher_with_page(self, query_model: NewTeacher, page_request: PageRequest):
        print(query_model)
        paging = await self.teachers_info_dao.query_teacher_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, NewTeacherRe)
        return paging_result