from mini_framework.databases.entities.dao_base import DAOBase
from sqlalchemy import select

from models.user_org_relation import UserOrgRelation


class UserOrgRelationDao(DAOBase):
    # 新增教师关键信息
    async def add_user_org_relation(self, user_org_relation):
        session = await self.master_db()
        session.add(user_org_relation)
        await session.commit()
        await session.refresh(user_org_relation)
        return user_org_relation

    async def get_user_org_relation_by_user_id(self, user_id):
        session = await self.slave_db()
        result = await session.execute(
            select(UserOrgRelation).where(UserOrgRelation.user_id == user_id))
        return result.scalar_one_or_none()

    async def get_user_org_relation_by_org_id(self, org_id):
        session = await self.slave_db()
        result = await session.execute(
            select(UserOrgRelation).where(UserOrgRelation.org_id == org_id))
        return result.scalar_one_or_none()
