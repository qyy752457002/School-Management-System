# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
import hashlib

import shortuuid
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.campus_dao import CampusDAO
from models.campus import Campus
from views.models.campus import Campus as CampusModel

from views.models.campus import CampusBaseInfo


@dataclass_inject
class CampusRule(object):
    campus_dao: CampusDAO

    async def get_campus_by_id(self, campus_id):
        campus_db = await self.campus_dao.get_campus_by_id(campus_id)
        # 可选 , exclude=[""]
        campus = orm_model_to_view_model(campus_db, CampusModel)
        return campus

    async def get_campus_by_campus_name(self, campus_name):
        campus_db = await self.campus_dao.get_campus_by_campus_name(
            campus_name)
        campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""])
        return campus

    async def add_campus(self, campus: CampusModel):
        exists_campus = await self.campus_dao.get_campus_by_campus_name(
            campus.campus_name)
        if exists_campus:
            raise Exception(f"校区{campus.campus_name}已存在")
        #  other_mapper={"password": "hash_password"},
        #                                              exclude=["first_name", "last_name"]
        campus_db = view_model_to_orm_model(campus, Campus,    exclude=["id"])

        campus_db.status = '正常'
        campus_db.created_uid = 0
        campus_db.updated_uid = 0

        campus_db = await self.campus_dao.add_campus(campus_db)
        campus = orm_model_to_view_model(campus_db, CampusModel, exclude=["created_at",'updated_at'])
        return campus

    async def update_campus(self, campus,ctype=1):
        # 默认 改 关键信息
        exists_campus = await self.campus_dao.get_campus_by_id(campus.id)
        if not exists_campus:
            raise Exception(f"校区{campus.id}不存在")
        if ctype==1:
            campus_db = Campus()
            campus_db.id = campus.id
            campus_db.campus_no = campus.campus_no
            campus_db.campus_name = campus.campus_name
            campus_db.block = campus.block
            campus_db.borough = campus.borough
            campus_db.campus_type = campus.campus_type
            campus_db.campus_operation_type = campus.campus_operation_type
            campus_db.campus_operation_type_lv2 = campus.campus_operation_type_lv2
            campus_db.campus_operation_type_lv3 = campus.campus_operation_type_lv3
            campus_db.campus_org_type = campus.campus_org_type
            campus_db.campus_level = campus.campus_level
        else:
            campus_db = Campus()
            campus_db.id = campus.id
            campus_db.campus_name=campus.campus_name
            campus_db.campus_short_name=campus.campus_short_name
            campus_db.campus_code=campus.campus_code
            campus_db.create_campus_date=campus.create_campus_date
            campus_db.founder_type=campus.founder_type
            campus_db.founder_name=campus.founder_name
            campus_db.urban_rural_nature=campus.urban_rural_nature
            campus_db.campus_operation_type=campus.campus_operation_type
            campus_db.campus_org_form=campus.campus_org_form
            campus_db.campus_operation_type_lv2=campus.campus_operation_type_lv2
            campus_db.campus_operation_type_lv3=campus.campus_operation_type_lv3
            campus_db.department_unit_number=campus.department_unit_number
            campus_db.sy_zones=campus.sy_zones
            campus_db.historical_evolution=campus.historical_evolution


        campus_db = await self.campus_dao.update_campus(campus_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""])
        return campus_db

    async def update_campus_byargs(self, campus,ctype=1):
        exists_campus = await self.campus_dao.get_campus_by_id(campus.id)
        if not exists_campus:
            raise Exception(f"校区{campus.id}不存在")
        need_update_list = []
        for key, value in campus.dict().items():
            if value:
                need_update_list.append(key)

        campus_db = await self.campus_dao.update_campus(campus, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""])
        return campus_db

    async def delete_campus(self, campus_id):
        exists_campus = await self.campus_dao.get_campus_by_id(campus_id)
        if not exists_campus:
            raise Exception(f"校区{campus_id}不存在")
        campus_db = await self.campus_dao.delete_campus(exists_campus)
        campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""],)
        return campus

    async def softdelete_campus(self, campus_id):
        exists_campus = await self.campus_dao.get_campus_by_id(campus_id)
        if not exists_campus:
            raise Exception(f"校区{campus_id}不存在")
        campus_db = await self.campus_dao.softdelete_campus(exists_campus)
        # campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""],)
        return campus_db

    async def get_all_campuss(self):
        return await self.campus_dao.get_all_campuss()

    async def get_campus_count(self):
        return await self.campus_dao.get_campus_count()

    async def query_campus_with_page(self, page_request: PageRequest, campus_name=None,
                                              campus_id=None,campus_no=None ):
        paging = await self.campus_dao.query_campus_with_page(campus_name, campus_id,campus_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, CampusModel)
        return paging_result


    async def update_campus_status(self, campus_id, status):
        exists_campus = await self.campus_dao.get_campus_by_id(campus_id)
        if not exists_campus:
            raise Exception(f"校区{campus_id}不存在")
        campus_db = await self.campus_dao.update_campus_status(exists_campus,status)
        # campus = orm_model_to_view_model(campus_db, CampusModel, exclude=[""],)
        return campus_db

