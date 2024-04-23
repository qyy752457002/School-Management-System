from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.talent_program import TalentProgram
from models.teachers import Teacher

class TalentProgramDAO(DAOBase):

	async def add_talent_program(self, talent_program: TalentProgram):
		session = await self.master_db()
		session.add(talent_program)
		await session.commit()
		await session.refresh(talent_program)
		return talent_program

	async def get_talent_program_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(TalentProgram))
		return result.scalar()

	async def delete_talent_program(self, talent_program: TalentProgram):
		session = await self.master_db()
		await session.delete(talent_program)
		await session.commit()

	async def get_talent_program_by_talent_program_id(self, talent_program_id):
		session = await self.slave_db()
		result = await session.execute(select(TalentProgram).where(TalentProgram.talent_program_id == talent_program_id))
		return result.scalar_one_or_none()

	async def query_talent_program_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(TalentProgram)
		
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_talent_program(self, talent_program, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(talent_program, *args)
		query = update(TalentProgram).where(TalentProgram.talent_program_id == talent_program.talent_program_id).values(**update_contents)
		return await self.update(session, query, talent_program, update_contents, is_commit=is_commit)


	async def get_all_talent_program(self,teacher_id):
		session = await self.slave_db()
		query = select(TalentProgram).join(Teacher,TalentProgram.teacher_id == Teacher.teacher_id).where(TalentProgram.teacher_id == teacher_id)
		result = await session.execute(query)
		return result.scalars().all()

