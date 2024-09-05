from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.tenant import Tenant


class TenantDAO(DAOBase):

	async def add_tenant(self, tenant: Tenant):
		session = await self.master_db()
		session.add(tenant)
		await session.commit()
		await session.refresh(tenant)
		return tenant

	async def get_tenant_count(self, ):
		session = await self.slave_db()
		result = await session.execute(select(func.count()).select_from(Tenant))
		return result.scalar()

	async def delete_tenant(self, tenant: Tenant):
		session = await self.master_db()
		await session.delete(tenant)
		await session.commit()

	async def get_tenant_by_id(self, id):
		session = await self.slave_db()
		result = await session.execute(select(Tenant).where(Tenant.id == id))
		return result.scalar_one_or_none()

	async def get_tenant_by_code(self, code):
		session = await self.slave_db()
		result = await session.execute(select(Tenant).where(Tenant.code == code).where(Tenant.is_deleted == False))
		return result.scalar_one_or_none()
	async def query_tenant_with_page(self, pageQueryModel, page_request: PageRequest):
		query = select(Tenant)
		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_tenant(self, tenant, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(tenant, *args)
		query = update(Tenant).where(Tenant.id == tenant.id).values(**update_contents)
		return await self.update(session, query, tenant, update_contents, is_commit=is_commit)
