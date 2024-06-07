import hashlib
from datetime import datetime

import shortuuid

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.institution_dao import InstitutionDAO
from models.institution import Institution
from views.models.institutions import Institutions  as InstitutionModel



@dataclass_inject
class InstitutionRule(object):
    institution_dao: InstitutionDAO

    async def get_institution_by_id(self, institution_id):
        institution_db = await self.institution_dao.get_institution_by_id(institution_id)
        # 可选 , exclude=[""]
        institution = orm_model_to_view_model(institution_db, InstitutionModel)
        return institution

    async def add_institution(self, institution: InstitutionModel):
        # exists_institution = await self.institution_dao.get_institution_by_id(
        #     institution.id)
        # if exists_institution:
        #     raise Exception(f"行政事业单位{institution.institution_name}已存在")


        institution_db = Institution()
        institution_db = view_model_to_orm_model(institution, Institution,    exclude=["id"])
        institution_db.updated_at = datetime.now()
        institution_db.created_at = datetime.now()



        institution_db = await self.institution_dao.add_institution(institution_db)
        print(institution_db,'插入suc')
        institution = orm_model_to_view_model(institution_db, InstitutionModel, exclude=[""])
        return institution

    async def update_institution(self, institution,ctype=1):
        exists_institution = await self.institution_dao.get_institution_by_id(institution.id)
        if not exists_institution:
            raise Exception(f"行政事业单位{institution.id}不存在")
        if ctype==1:
            institution_db = Institution()
            institution_db.id = institution.id
            institution_db.institution_no = institution.institution_no
            institution_db.institution_name = institution.institution_name
            institution_db.block = institution.block
            institution_db.borough = institution.borough
            institution_db.institution_type = institution.institution_type
            institution_db.institution_operation_type = institution.institution_operation_type
            institution_db.institution_operation_type_lv2 = institution.institution_operation_type_lv2
            institution_db.institution_operation_type_lv3 = institution.institution_operation_type_lv3
            institution_db.institution_org_type = institution.institution_org_type
            institution_db.institution_level = institution.institution_level
        else:
            institution_db = Institution()
            institution_db.id = institution.id
            institution_db.institution_name=institution.institution_name
            institution_db.institution_short_name=institution.institution_short_name
            institution_db.institution_code=institution.institution_code
            institution_db.create_institution_date=institution.create_institution_date
            institution_db.founder_type=institution.founder_type
            institution_db.founder_name=institution.founder_name
            institution_db.urban_rural_nature=institution.urban_rural_nature
            institution_db.institution_operation_type=institution.institution_operation_type
            institution_db.institution_org_form=institution.institution_org_form
            institution_db.institution_operation_type_lv2=institution.institution_operation_type_lv2
            institution_db.institution_operation_type_lv3=institution.institution_operation_type_lv3
            institution_db.department_unit_number=institution.department_unit_number
            institution_db.sy_zones=institution.sy_zones
            institution_db.historical_evolution=institution.historical_evolution


        institution_db = await self.institution_dao.update_institution(institution_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # institution = orm_model_to_view_model(institution_db, InstitutionModel, exclude=[""])
        return institution_db

    async def softdelete_institution(self, institution_id):
        exists_institution = await self.institution_dao.get_institution_by_id(institution_id)
        if not exists_institution:
            raise Exception(f"行政事业单位{institution_id}不存在")
        institution_db = await self.institution_dao.softdelete_institution(exists_institution)
        # institution = orm_model_to_view_model(institution_db, InstitutionModel, exclude=[""],)
        return institution_db


    async def get_institution_count(self):
        return await self.institution_dao.get_institution_count()

    async def query_institution_with_page(self, page_request: PageRequest, institution_name=None,
                                              institution_id=None,institution_no=None ):
        paging = await self.institution_dao.query_institution_with_page(institution_name, institution_id,institution_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, InstitutionModel, {"create_institution_date": "create_date","web_url": "website_url",})
        return paging_result

