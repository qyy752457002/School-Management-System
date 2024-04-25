from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.annual_review import AnnualReview
from models.teachers import Teacher


class AnnualReviewDAO(DAOBase):

	async def add_annual_review(self, annual_review: AnnualReview):
		session = await self.master_db()
		session.add(annual_review)
		await session.commit()
		await session.refresh(annual_review)
		return annual_review

	async def get_annual_review_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(AnnualReview))
		return result.scalar()

	async def delete_annual_review(self, annual_review: AnnualReview):
		session = await self.master_db()
		return await self.delete(session, annual_review)

	async def get_annual_review_by_annual_review_id(self, annual_review_id):
		session = await self.slave_db()
		result = await session.execute(select(AnnualReview).where(AnnualReview.annual_review_id == annual_review_id))
		return result.scalar_one_or_none()

	async def query_annual_review_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(AnnualReview)
		
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_annual_review(self, annual_review, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(annual_review, *args)
		query = update(AnnualReview).where(AnnualReview.annual_review_id == annual_review.annual_review_id).values(**update_contents)
		return await self.update(session, query, annual_review, update_contents, is_commit=is_commit)


	async def get_all_annual_review(self,teacher_id):
		session = await self.slave_db()
		query = select(AnnualReview).join(Teacher,AnnualReview.teacher_id == Teacher.teacher_id).where(AnnualReview.teacher_id == teacher_id)
		result = await session.execute(query)
		return result.scalars().all()

