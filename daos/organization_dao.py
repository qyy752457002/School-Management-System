from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.web.std_models.page import PageRequest
from sqlalchemy import select, func, update

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
        await self.delete(session, organization)
        await session.commit()

    async def get_organization_by_id(self, id, use_master=False):
        if use_master:
            session = await self.master_db()
        else:
            session = await self.slave_db()
        result = await session.execute(select(Organization).where(Organization.id == int(id)))
        return result.scalar_one_or_none()

    async def get_organization_by_name(self, name, organization):
        session = await self.slave_db()
        result = await session.execute(select(Organization).where(Organization.org_name == name).where(
            Organization.parent_id == organization.parent_id).where(
            Organization.school_id == organization.school_id).where(Organization.is_deleted == False))
        return result.scalar_one_or_none()

    async def get_organization_by_name_and_school_id(self, org_name, school_id):
        session = await self.slave_db()
        result = await session.execute(select(Organization).where(Organization.org_name == org_name).where(
            Organization.school_id == school_id).where(Organization.is_deleted == False))
        return result.scalar_one_or_none()

    async def query_organization_with_page(self, page_request: PageRequest, parent_id, school_id):
        query = select(Organization).where(Organization.is_deleted == False)
        if parent_id:
            if isinstance(parent_id, list):
                query = query.where(Organization.parent_id.in_(parent_id))
            else:
                query = query.where(Organization.parent_id == parent_id)
        if school_id:
            query = query.where(Organization.school_id == school_id)

        ### �˴���д��ѯ����

        paging = await self.query_page(query, page_request)
        return paging

    async def update_organization(self, organization, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(organization, *args)
        query = update(Organization).where(Organization.id == organization.id).values(**update_contents)
        return await self.update(session, query, organization, update_contents, is_commit=is_commit)

    async def get_child_organization_ids(self, organization_ids):
        session = await self.slave_db()
        result = await session.execute(select(Organization).where(Organization.parent_id.in_(organization_ids)))
        res = result.scalars().all()
        return [i.id for i in res]

    async def delete_organization_by_ids(self, organization_ids, ):
        session = await self.master_db()
        query = update(Organization).where(Organization.id.in_(organization_ids)).values(is_deleted=True)
        return await self.update(session, query, Organization, {'is_deleted': True}, )

    async def update_organization_increment_member_cnt(self, organization, *args, is_commit=True):
        session = await self.master_db()
        query = update(Organization).where(Organization.id == int(organization.id)).values(
            {Organization.member_cnt: Organization.member_cnt + 1})

        await session.execute(query)
        # await session.query(Organization).filter_by(id=organization.id).update({Organization.value: Organization.value + 1})
        await session.commit()

    async def get_organization_by_org_name(self, org_name):
        session = await self.slave_db()
        result = await session.execute(
            select(Organization).where(Organization.org_name == org_name, Organization.is_deleted == False))
        return result.first()
