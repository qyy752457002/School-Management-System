from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.organization import Organization
from models.organization_members import OrganizationMembers
from models.teachers import Teacher
from models.teachers_info import TeacherInfo


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
		await self.delete(session,organization_members)
		await session.commit()

	async def get_organization_members_by_id(self, id,use_master=False):
		if use_master:
			session = await self.master_db()
		else:
			session = await self.slave_db()
		result = await session.execute(select(OrganizationMembers).where(OrganizationMembers.id == id))
		return result.scalar_one_or_none()

	async def get_organization_members_by_param(self, organization:OrganizationMembers):
		session = await self.slave_db()
		query = select(OrganizationMembers)
		if organization.teacher_id:
			query = query.where(OrganizationMembers.teacher_id == organization.teacher_id)
		if organization.org_id:
			query = query.where(OrganizationMembers.org_id == organization.org_id)
		if organization.member_type:
			query = query.where(OrganizationMembers.member_type == organization.member_type)

		result = await session.execute(  query)
		return result.scalar_one_or_none()
	async def query_organization_members_with_page(self,  page_request: PageRequest,parent_id , school_id,teacher_name,teacher_no,mobile,birthday):
		query = (select(OrganizationMembers.id,
						OrganizationMembers.org_id,
						OrganizationMembers.teacher_id,
						OrganizationMembers.member_type,
						Teacher.teacher_name,
						Teacher.teacher_date_of_birth,
						Teacher.teacher_gender,
						Teacher.teacher_id_type,
						Teacher.teacher_id_number,
						# Teacher.tea,
						).select_from(OrganizationMembers)
				 .join(Organization, OrganizationMembers.org_id == Organization.id, isouter=True)
				 .join(Teacher, OrganizationMembers.teacher_id == Teacher.teacher_id, isouter=True)
				 .join(TeacherInfo, TeacherInfo.teacher_id == Teacher.teacher_id, isouter=True)
				 )
		if parent_id:
			if isinstance(parent_id, list):
				query = query.where(Organization.id.in_(parent_id))
			else:
				query = query.where(Organization.id == parent_id)

		if school_id:
			query = query.where(Organization.school_id == school_id)
		if teacher_name:
			query = query.where(Teacher.teacher_name.like(f'%{teacher_name}%'))
		if teacher_no:
			query = query.where(TeacherInfo.teacher_number.like(f'%{teacher_no}%'))
		if mobile:
			# query = query.where(Teacher.mobile.like(f'%{mobile}%'))
			pass
		if birthday:
			query = query.where(Teacher.teacher_date_of_birth.like(f'%{birthday}%'))

		
		### �˴���д��ѯ����
		
		paging = await self.query_page(query, page_request)
		return paging

	async def update_organization_members(self, organization_members, *args, is_commit=True):
		session = await self.master_db()
		update_contents = get_update_contents(organization_members, *args)
		query = update(OrganizationMembers).where(OrganizationMembers.id == organization_members.id).values(**update_contents)
		return await self.update(session, query, organization_members, update_contents, is_commit=is_commit)

	async def delete_organization_members_by_teacher_id(self, teacher_id, is_commit=True):
		session = await self.master_db()
		update_contents = {"is_deleted":True}
		query = update(OrganizationMembers).where(OrganizationMembers.teacher_id ==teacher_id).values(is_deleted=True)
		return await self.update(session, query, OrganizationMembers, update_contents, is_commit=is_commit)
