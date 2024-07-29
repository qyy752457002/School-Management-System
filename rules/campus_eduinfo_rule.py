# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.campus_eduinfo import CampusEduinfoNotFoundError
from daos.campus_eduinfo_dao import CampusEduinfoDAO
from models.campus_eduinfo import CampusEduinfo
from views.models.campus_eduinfo import CampusEduInfo  as CampusEduinfoModel



@dataclass_inject
class CampusEduinfoRule(object):
    campus_eduinfo_dao: CampusEduinfoDAO

    async def get_campus_eduinfo_by_id(self, campus_eduinfo_id):
        campus_eduinfo_db = await self.campus_eduinfo_dao.get_campus_eduinfo_by_id(campus_eduinfo_id)
        # 可选 , exclude=[""]
        campus = orm_model_to_view_model(campus_eduinfo_db, CampusEduinfoModel)
        return campus

    async def get_campus_eduinfo_by_campus_id(self, campus_eduinfo_id):
        campus_eduinfo_db = await self.campus_eduinfo_dao.get_campus_eduinfo_by_campus_id(campus_eduinfo_id)
        # 可选 , exclude=[""]
        campus = orm_model_to_view_model(campus_eduinfo_db, CampusEduinfoModel)
        return campus

    async def add_campus_eduinfo(self, campus: CampusEduinfoModel,convertmodel=True):
        exists_campus = await self.campus_eduinfo_dao.get_campus_eduinfo_by_campus_id(
            campus.campus_id)
        if exists_campus:
            raise Exception(f"校区教育信息{campus.campus_id}已存在")

        if convertmodel:
            campus_eduinfo_db = view_model_to_orm_model(campus, CampusEduinfo,    exclude=["id"])

        else:
            campus_eduinfo_db = CampusEduinfo()
            campus_eduinfo_db.id = None
            campus_eduinfo_db.campus_id= campus.campus_id

        campus_eduinfo_db.deleted = 0
        campus_eduinfo_db.status = '正常'
        campus_eduinfo_db.created_uid = 0
        campus_eduinfo_db.updated_uid = 0
        campus_eduinfo_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        # campus_eduinfo_db = view_model_to_orm_model(campus, CampusEduinfo,    exclude=["id"])

        campus_eduinfo_db = await self.campus_eduinfo_dao.add_campus_eduinfo(campus_eduinfo_db)
        campus = orm_model_to_view_model(campus_eduinfo_db, CampusEduinfoModel, exclude=["created_at",'updated_at'])
        return campus

    async def update_campus_eduinfo(self, campus,ctype=1):
        exists_campus = await self.campus_eduinfo_dao.get_campus_eduinfo_by_id(campus.id)
        if not exists_campus:
            raise Exception(f"校区教育信息{campus.id}不存在")
        if ctype==1:
            campus_eduinfo_db = CampusEduinfo()
            campus_eduinfo_db.id = campus.id
            campus_eduinfo_db.campus_eduinfo_no = campus.campus_eduinfo_no
            campus_eduinfo_db.campus_eduinfo_name = campus.campus_eduinfo_name
            campus_eduinfo_db.block = campus.block
            campus_eduinfo_db.borough = campus.borough
            campus_eduinfo_db.campus_eduinfo_type = campus.campus_eduinfo_type
            campus_eduinfo_db.campus_eduinfo_operation_type = campus.campus_eduinfo_operation_type
            campus_eduinfo_db.campus_eduinfo_operation_type_lv2 = campus.campus_eduinfo_operation_type_lv2
            campus_eduinfo_db.campus_eduinfo_operation_type_lv3 = campus.campus_eduinfo_operation_type_lv3
            campus_eduinfo_db.campus_eduinfo_org_type = campus.campus_eduinfo_org_type
            campus_eduinfo_db.campus_eduinfo_level = campus.campus_eduinfo_level
        else:
            campus_eduinfo_db = CampusEduinfo()
            campus_eduinfo_db.id = campus.id
            campus_eduinfo_db.campus_eduinfo_name=campus.campus_eduinfo_name
            campus_eduinfo_db.campus_eduinfo_short_name=campus.campus_eduinfo_short_name
            campus_eduinfo_db.campus_eduinfo_code=campus.campus_eduinfo_code
            campus_eduinfo_db.create_campus_eduinfo_date=campus.create_campus_eduinfo_date
            campus_eduinfo_db.founder_type=campus.founder_type
            campus_eduinfo_db.founder_name=campus.founder_name
            campus_eduinfo_db.urban_rural_nature=campus.urban_rural_nature
            campus_eduinfo_db.campus_eduinfo_operation_type=campus.campus_eduinfo_operation_type
            campus_eduinfo_db.campus_eduinfo_org_form=campus.campus_eduinfo_org_form
            campus_eduinfo_db.campus_eduinfo_operation_type_lv2=campus.campus_eduinfo_operation_type_lv2
            campus_eduinfo_db.campus_eduinfo_operation_type_lv3=campus.campus_eduinfo_operation_type_lv3
            campus_eduinfo_db.department_unit_number=campus.department_unit_number
            campus_eduinfo_db.sy_zones=campus.sy_zones
            campus_eduinfo_db.historical_evolution=campus.historical_evolution


        campus_eduinfo_db = await self.campus_eduinfo_dao.update_campus_eduinfo(campus_eduinfo_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # campus = orm_model_to_view_model(campus_eduinfo_db, CampusEduinfoModel, exclude=[""])
        return campus_eduinfo_db

    async def softdelete_campus_eduinfo(self, campus_eduinfo_id):
        exists_campus = await self.campus_eduinfo_dao.get_campus_eduinfo_by_id(campus_eduinfo_id)
        if not exists_campus:
            raise Exception(f"校区教育信息{campus_eduinfo_id}不存在")
        campus_eduinfo_db = await self.campus_eduinfo_dao.softdelete_campus_eduinfo(exists_campus)
        # campus = orm_model_to_view_model(campus_eduinfo_db, CampusEduinfoModel, exclude=[""],)
        return campus_eduinfo_db


    async def get_campus_eduinfo_count(self):
        return await self.campus_eduinfo_dao.get_campus_eduinfo_count()

    async def query_campus_eduinfo_with_page(self, page_request: PageRequest, campus_eduinfo_name=None,
                                              campus_eduinfo_id=None,campus_eduinfo_no=None ):
        paging = await self.campus_eduinfo_dao.query_campus_eduinfo_with_page(campus_eduinfo_name, campus_eduinfo_id,campus_eduinfo_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, CampusEduinfoModel)
        return paging_result

    async def update_campus_eduinfo_byargs(self, campus_eduinfo,ctype=1):
        if campus_eduinfo.campus_id>0:
            exists_campus_eduinfo = await self.campus_eduinfo_dao.get_campus_eduinfo_by_campus_id(campus_eduinfo.campus_id)


        else:

            exists_campus_eduinfo = await self.campus_eduinfo_dao.get_campus_eduinfo_by_id(campus_eduinfo.id)
        if not exists_campus_eduinfo:
            raise CampusEduinfoNotFoundError()
        need_update_list = []
        for key, value in campus_eduinfo.dict().items():
            if value:
                need_update_list.append(key)

        campus_eduinfo_db = await self.campus_eduinfo_dao.update_campus_eduinfo_byargs(campus_eduinfo, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        return campus_eduinfo_db

