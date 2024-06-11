from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.organization_members import OrganizationMembers


class OrganizationMembersDAO(DAOBase):

	async def add_organization_members(self, organization_members: OrganizationMembers):
		session = await self.master_db()
		session.add(organization_members)
		await session.commit()
		await session.refresh(organization_members)
		return organization_members

	async def get_organization_members_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(OrganizationMembers))
		return result.scalar()

	async def delete_organization_members(self, organization_members: OrganizationMembers):
		session = await self.master_db()
		await session.delete(organization_members)
		await session.commit()

	async def get_organization_members_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(OrganizationMembers).where(OrganizationMembers.id == id))
		return result.scalar_one_or_none()

	async def get_organization_members_by_param(self, organization:OrganizationMembers):
		session = await self.slave_db()
		result = await session.execute(select(OrganizationMembers).where(OrganizationMembers.teacher_id == organization.teacher_id).where(OrganizationMembers.org_id == organization.org_id).where(OrganizationMembers.member_type == organization.member_type))
		return result.scalar_one_or_none()
	async def query_organization_members_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(OrganizationMembers)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_organization_members(self, organization_members, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(organization_members, *args)
		query = update(OrganizationMembers).where(OrganizationMembers.id == organization_members.id).values(**update_contents)
		return await self.update(session, query, organization_members, update_contents, is_commit=is_commit)
