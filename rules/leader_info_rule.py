# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.LeaderInfo_dao import LeaderInfoDAO
from models.leader_info import LeaderInfo
from views.models.leader_info import LeaderInfo  as LeaderInfoModel



@dataclass_inject
class LeaderInfoRule(object):
    leader_info_dao: LeaderInfoDAO

    async def get_leader_info_by_id(self, leader_info_id):
        leader_info_db = await self.leader_info_dao.get_leader_info_by_id(leader_info_id)
        # 可选 , exclude=[""]
        leader_info = orm_model_to_view_model(leader_info_db, LeaderInfoModel)
        return leader_info

    async def add_leader_info(self, leader_info: LeaderInfoModel):
        exists_leader_info = await self.leader_info_dao.get_leader_info_by_leader_info_name(
            leader_info.leader_name)
        if exists_leader_info:
            raise Exception(f"领导信息{leader_info.leader_name}已存在")
        leader_info_db = view_model_to_orm_model(leader_info, LeaderInfo,    exclude=["id"])

        leader_info_db = await self.leader_info_dao.add_leader_info(leader_info_db)
        leader_info = orm_model_to_view_model(leader_info_db, LeaderInfoModel, exclude=["created_at",'updated_at'])
        return leader_info

    async def update_leader_info(self, leader_info,ctype=1):
        exists_leader_info = await self.leader_info_dao.get_leader_info_by_id(leader_info.id)
        if not exists_leader_info:
            raise Exception(f"领导信息{leader_info.id}不存在")
        need_update_list = []
        for key, value in leader_info.dict().items():
            if value:
                need_update_list.append(key)

        leader_info_db = await self.leader_info_dao.update_leader_info_byargs(leader_info, *need_update_list)


        # leader_info_db = await self.leader_info_dao.update_leader_info(leader_info_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # leader_info = orm_model_to_view_model(leader_info_db, LeaderInfoModel, exclude=[""])
        return leader_info_db

    async def softdelete_leader_info(self, leader_info_id):
        exists_leader_info = await self.leader_info_dao.get_leader_info_by_id(leader_info_id)
        if not exists_leader_info:
            raise Exception(f"领导信息{leader_info_id}不存在")
        leader_info_db = await self.leader_info_dao.softdelete_leader_info(exists_leader_info)
        # leader_info = orm_model_to_view_model(leader_info_db, LeaderInfoModel, exclude=[""],)
        return leader_info_db


    async def get_leader_info_count(self):
        return await self.leader_info_dao.get_leader_info_count()

    async def query_leader_info_with_page(self, page_request: PageRequest, leader_info_name=None,
                                              leader_info_id=None,leader_info_no=None ):
        paging = await self.leader_info_dao.query_leader_info_with_page(
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, LeaderInfoModel)
        return paging_result

