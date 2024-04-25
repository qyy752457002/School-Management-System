from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.talent_program_dao import TalentProgramDAO
from models.talent_program import TalentProgram
from views.models.teacher_extend import TalentProgramModel, TalentProgramUpdateModel
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError


@dataclass_inject
class TalentProgramRule(object):
    talent_program_dao: TalentProgramDAO
    teachers_dao: TeachersDao

    async def get_talent_program_by_talent_program_id(self, talent_program_id):
        talent_program_db = await self.talent_program_dao.get_talent_program_by_talent_program_id(talent_program_id)
        talent_program = orm_model_to_view_model(talent_program_db, TalentProgramModel)
        return talent_program

    async def add_talent_program(self, talent_program: TalentProgramModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(talent_program.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        talent_program_db = view_model_to_orm_model(talent_program, TalentProgram)
        talent_program_db = await self.talent_program_dao.add_talent_program(talent_program_db)
        talent_program = orm_model_to_view_model(talent_program_db, TalentProgramModel)
        return talent_program

    async def delete_talent_program(self, talent_program_id):
        exists_talent_program = await self.talent_program_dao.get_talent_program_by_talent_program_id(talent_program_id)
        if not exists_talent_program:
            raise Exception(f"编号为的{talent_program_id}talent_program不存在")
        talent_program_db = await self.talent_program_dao.delete_talent_program(exists_talent_program)
        talent_program = orm_model_to_view_model(talent_program_db, TalentProgramModel, exclude=[""])
        return talent_program

    async def update_talent_program(self, talent_program: TalentProgramUpdateModel):
        exists_talent_program_info = await self.talent_program_dao.get_talent_program_by_talent_program_id(
            talent_program.talent_program_id)
        if not exists_talent_program_info:
            raise Exception(f"编号为{talent_program.talent_program_id}的talent_program不存在")
        need_update_list = []
        for key, value in talent_program.dict().items():
            if value:
                need_update_list.append(key)
        talent_program = await self.talent_program_dao.update_talent_program(talent_program, *need_update_list)
        return talent_program

    async def get_all_talent_program(self, teacher_id):
        talent_program_db = await self.talent_program_dao.get_all_talent_program(teacher_id)
        #          talent_program = orm_model_to_view_model(talent_program_db, TalentProgramModel, exclude=[""])
        talent_program = []
        for item in talent_program_db:
            talent_program.append(orm_model_to_view_model(item, TalentProgramModel))
        return talent_program_db


