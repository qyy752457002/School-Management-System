# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest

from business_exceptions.campus_communication import CampusCommunicationNotFoundError
from daos.campus_communication_dao import CampusCommunicationDAO
from models.campus_communication import CampusCommunication
from views.models.campus_communications import CampusCommunications  as CampusCommunicationModel



@dataclass_inject
class CampusCommunicationRule(object):
    campus_communication_dao: CampusCommunicationDAO

    async def get_campus_communication_by_id(self, campus_communication_id):
        campus_communication_db = await self.campus_communication_dao.get_campus_communication_by_id(campus_communication_id)
        # 可选 , exclude=[""]
        campus = orm_model_to_view_model(campus_communication_db, CampusCommunicationModel)
        return campus
    async def get_campus_communication_by_campus_id(self, campus_communication_id):
        campus_communication_db = await self.campus_communication_dao.get_campus_communication_by_campus_id(campus_communication_id)
        # 可选 , exclude=[""]
        campus = orm_model_to_view_model(campus_communication_db, CampusCommunicationModel)
        return campus

    async def add_campus_communication(self, campus: CampusCommunicationModel,convertmodel=True):
        exists_campus = await self.campus_communication_dao.get_campus_communication_by_id(
            campus.campus_id)
        if exists_campus:
            raise Exception(f"校区通信信息{campus.campus_communication_name}已存在")

        if convertmodel:
            campus_communication_db = view_model_to_orm_model(campus, CampusCommunication,    exclude=["id"])

        else:
            campus_communication_db = CampusCommunication()
            campus_communication_db.id = None
            campus_communication_db.campus_id= campus.campus_id

        campus_communication_db.deleted = 0
        campus_communication_db.status = '正常'
        campus_communication_db.created_uid = 0
        campus_communication_db.updated_uid = 0

        # campus_communication_db = view_model_to_orm_model(campus, CampusCommunication,    exclude=["id"])

        campus_communication_db = await self.campus_communication_dao.add_campus_communication(campus_communication_db)
        campus = orm_model_to_view_model(campus_communication_db, CampusCommunicationModel, exclude=["created_at",'updated_at'])
        return campus

    async def update_campus_communication(self, campus,ctype=1):
        exists_campus = await self.campus_communication_dao.get_campus_communication_by_id(campus.id)
        if not exists_campus:
            raise Exception(f"校区通信信息{campus.id}不存在")
        if ctype==1:
            campus_communication_db = CampusCommunication()
            campus_communication_db.id = campus.id
            campus_communication_db.campus_communication_no = campus.campus_communication_no
            campus_communication_db.campus_communication_name = campus.campus_communication_name
            campus_communication_db.block = campus.block
            campus_communication_db.borough = campus.borough
            campus_communication_db.campus_communication_type = campus.campus_communication_type
            campus_communication_db.campus_communication_operation_type = campus.campus_communication_operation_type
            campus_communication_db.campus_communication_operation_type_lv2 = campus.campus_communication_operation_type_lv2
            campus_communication_db.campus_communication_operation_type_lv3 = campus.campus_communication_operation_type_lv3
            campus_communication_db.campus_communication_org_type = campus.campus_communication_org_type
            campus_communication_db.campus_communication_level = campus.campus_communication_level
        else:
            campus_communication_db = CampusCommunication()
            campus_communication_db.id = campus.id
            campus_communication_db.campus_communication_name=campus.campus_communication_name
            campus_communication_db.campus_communication_short_name=campus.campus_communication_short_name
            campus_communication_db.campus_communication_code=campus.campus_communication_code
            campus_communication_db.create_campus_communication_date=campus.create_campus_communication_date
            campus_communication_db.founder_type=campus.founder_type
            campus_communication_db.founder_name=campus.founder_name
            campus_communication_db.urban_rural_nature=campus.urban_rural_nature
            campus_communication_db.campus_communication_operation_type=campus.campus_communication_operation_type
            campus_communication_db.campus_communication_org_form=campus.campus_communication_org_form
            campus_communication_db.campus_communication_operation_type_lv2=campus.campus_communication_operation_type_lv2
            campus_communication_db.campus_communication_operation_type_lv3=campus.campus_communication_operation_type_lv3
            campus_communication_db.department_unit_number=campus.department_unit_number
            campus_communication_db.sy_zones=campus.sy_zones
            campus_communication_db.historical_evolution=campus.historical_evolution


        campus_communication_db = await self.campus_communication_dao.update_campus_communication(campus_communication_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # campus = orm_model_to_view_model(campus_communication_db, CampusCommunicationModel, exclude=[""])
        return campus_communication_db

    async def softdelete_campus_communication(self, campus_communication_id):
        exists_campus = await self.campus_communication_dao.get_campus_communication_by_id(campus_communication_id)
        if not exists_campus:
            raise Exception(f"校区通信信息{campus_communication_id}不存在")
        campus_communication_db = await self.campus_communication_dao.softdelete_campus_communication(exists_campus)
        # campus = orm_model_to_view_model(campus_communication_db, CampusCommunicationModel, exclude=[""],)
        return campus_communication_db


    async def get_campus_communication_count(self):
        return await self.campus_communication_dao.get_campus_communication_count()

    async def query_campus_communication_with_page(self, page_request: PageRequest, campus_communication_name=None,
                                              campus_communication_id=None,campus_communication_no=None ):
        paging = await self.campus_communication_dao.query_campus_communication_with_page(campus_communication_name, campus_communication_id,campus_communication_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, CampusCommunicationModel)
        return paging_result

    async def update_campus_communication_byargs(self, campus_communication,ctype=1):
        if campus_communication.campus_id>0:
            exists_campus_communication = await self.campus_communication_dao.get_campus_communication_by_campus_id(campus_communication.campus_id)


        else:

            exists_campus_communication = await self.campus_communication_dao.get_campus_communication_by_id(campus_communication.id)
        if not exists_campus_communication:
            raise CampusCommunicationNotFoundError()
        need_update_list = []
        for key, value in campus_communication.dict().items():
            if value:
                need_update_list.append(key)

        campus_communication_db = await self.campus_communication_dao.update_campus_communication_byargs(campus_communication, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        return campus_communication_db

