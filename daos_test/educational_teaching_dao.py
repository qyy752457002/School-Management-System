from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.educational_teaching import EducationalTeaching


class EducationalTeachingDAO(DAOBase):

	async def add_educationalteaching(self, educationalteaching: EducationalTeaching):
		session = await self.master_db()
		session.add(educationalteaching)
		await session.commit()
		await session.refresh(educationalteaching)
		return educationalteaching

	async def get_educationalteaching_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(EducationalTeaching))
		return result.scalar()

	async def delete_educationalteaching(self, educationalteaching: EducationalTeaching):
		session = await self.master_db()
		await session.delete(educationalteaching)
		await session.commit()

	async def get_educationalteaching_by_educational_teaching_id(self, educational_teaching_id):
		session = await self.slave_db()
		result = await session.execute(select(EducationalTeaching).where(EducationalTeaching.educational_teaching_id == educational_teaching_id))
		return result.scalar_one_or_none()

	async def query_educationalteaching_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(EducationalTeaching)
		
		### 此处填写查询条件
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_educationalteaching(self, educationalteaching, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(educationalteaching, *args)
		query = update(EducationalTeaching).where(EducationalTeaching.educational_teaching_id == educationalteaching.educational_teaching_id).values(**update_contents)
		return await self.update(session, query, educationalteaching, update_contents, is_commit=is_commit)
