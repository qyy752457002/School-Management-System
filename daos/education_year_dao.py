from sqlalchemy import select, func, update, asc
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.education_year import EducationYear


class EducationYearDAO(DAOBase):

	async def add_education_year(self, education_year: EducationYear):
		session = await self.master_db()
		session.add(education_year)
		await session.commit()
		await session.refresh(education_year)
		return education_year

	async def get_education_year_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(EducationYear))
		return result.scalar()

	async def delete_education_year(self, education_year: EducationYear):
		session = await self.master_db()
		await session.delete(education_year)
		await session.commit()

	async def get_education_year_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(EducationYear).where(EducationYear.id == id))
		return result.scalar_one_or_none()

	async def query_education_year_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(EducationYear)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_education_year(self, education_year, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(education_year, *args)
		query = update(EducationYear).where(EducationYear.id == education_year.id).values(**update_contents)
		return await self.update(session, query, education_year, update_contents, is_commit=is_commit)

	async def query_education_year_with_args(self,  school_type, city, district,):
		query = (select(EducationYear
						).select_from( EducationYear).order_by(asc(EducationYear.id)))
		query = query.where(EducationYear.is_deleted == False)

		if school_type:
			query = query.where(EducationYear.school_type == school_type)
		if city:
			query = query.where(EducationYear.city == city)
		if district:
			query = query.where(EducationYear.district == district)

		session = await self.slave_db()
		columns=query.columns.keys()

		result = await session.execute(query)
		# columns=result.keys()
		result_items= result.all()


		# 将元组列表转换为字典列表
		nl = [ ]
		dict_result_items = [dict(zip(columns, item)) for item in result_items]
		# for item in dict_result_items:
		# 	# item['id'] = item.pop('id')
		# 	nl.append( item.values() )

		return dict_result_items
