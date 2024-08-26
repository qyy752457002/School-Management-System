from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from daos.user_org_relation_dao import UserOrgRelationDao
from models.user_org_relation import UserOrgRelation


@dataclass_inject
class UserOrgRelationRule:
    def __init__(self):
        self.user_org_relation_dao = get_injector(UserOrgRelationDao)

    async def add_user_org_relation(self, supervisor_id, org_id):
        """
        新增教师关键信息
        :param user_org_relation:
        :return:
        """
        user_org_relation = UserOrgRelation(user_id=int(supervisor_id), org_id=org_id)
        user_org_relation.id = SnowflakeIdGenerator(1, 1).generate_id()
        exit_user_org_relation = await self.user_org_relation_dao.get_user_org_relation_by_user_id(
            user_org_relation.user_id)
        if exit_user_org_relation:
            await self.user_org_relation_dao.delete_user_org_relation(exit_user_org_relation)
        await self.user_org_relation_dao.add_user_org_relation(user_org_relation)
        return

    async def get_user_org_relation_by_user_id(self, user_id):
        """
        根据用户ID获取用户关系
        :param user_id:
        :return:
        """
        user_org_relation = await self.user_org_relation_dao.get_user_org_relation_by_user_id(user_id)
        return orm_model_to_view_model(user_org_relation)

    async def get_user_org_relation_by_org_id(self, org_id):
        """
        根据机构ID获取用户关系
        :param org_id:
        :return:
        """
        user_org_relation = await self.user_org_relation_dao.get_user_org_relation_by_org_id(org_id)
        return orm_model_to_view_model(user_org_relation)

    async def delete_user_org_relation(self, user_org_relation):
        """
        删除用户关系
        :param user_org_relation:
        :return:
        """
        user_org_relation = view_model_to_orm_model(user_org_relation)
        return await self.user_org_relation_dao.delete_user_org_relation(user_org_relation)
