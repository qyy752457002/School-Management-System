from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.organization import Organization


class OrganizationDAO(DAOBase):

	async def add_organization(self, organization: Organization):
		session = await self.master_db()
		session.add(organization)
		await session.commit()
		await session.refresh(organization)
		return organization

	async def get_organization_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(Organization))
		return result.scalar()

	async def delete_organization(self, organization: Organization):
		session = await self.master_db()
		await session.delete(organization)
		await session.commit()

	async def get_organization_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(Organization).where(Organization.id == id))
		return result.scalar_one_or_none()

	async def get_organization_by_name(self, name):
		session = await self.slave_db()
		result = await session.execute(select(Organization).where(Organization.org_name == name))
		return result.scalar_one_or_none()

	async def query_organization_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(Organization)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_organization(self, organization, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(organization, *args)
		query = update(Organization).where(Organization.id == organization.id).values(**update_contents)
		return await self.update(session, query, organization, update_contents, is_commit=is_commit)
