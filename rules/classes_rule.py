# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.class_dao import ClassesDAO
from models.classes import Classes
from views.models.classes import CampusEduInfo  as ClassesModel



@dataclass_inject
class ClassesRule(object):
    classes_dao: ClassesDAO

    async def get_classes_by_id(self, classes_id):
        classes_db = await self.classes_dao.get_classes_by_id(classes_id)
        # 可选 , exclude=[""]
        campus = orm_model_to_view_model(classes_db, ClassesModel)
        return campus

    async def add_classes(self, campus: ClassesModel):
        exists_campus = await self.classes_dao.get_classes_by_id(
            campus.campus_id)
        if exists_campus:
            raise Exception(f"校区教育信息{campus.classes_name}已存在")
        classes_db = view_model_to_orm_model(campus, Classes,    exclude=["id"])

        classes_db = await self.classes_dao.add_classes(classes_db)
        campus = orm_model_to_view_model(classes_db, ClassesModel, exclude=["created_at",'updated_at'])
        return campus

    async def update_classes(self, campus,ctype=1):
        exists_campus = await self.classes_dao.get_classes_by_id(campus.id)
        if not exists_campus:
            raise Exception(f"校区教育信息{campus.id}不存在")
        if ctype==1:
            classes_db = Classes()
            classes_db.id = campus.id
            classes_db.classes_no = campus.classes_no
            classes_db.classes_name = campus.classes_name
            classes_db.block = campus.block
            classes_db.borough = campus.borough
            classes_db.classes_type = campus.classes_type
            classes_db.classes_operation_type = campus.classes_operation_type
            classes_db.classes_operation_type_lv2 = campus.classes_operation_type_lv2
            classes_db.classes_operation_type_lv3 = campus.classes_operation_type_lv3
            classes_db.classes_org_type = campus.classes_org_type
            classes_db.classes_level = campus.classes_level
        else:
            classes_db = Classes()
            classes_db.id = campus.id
            classes_db.classes_name=campus.classes_name
            classes_db.classes_short_name=campus.classes_short_name
            classes_db.classes_code=campus.classes_code
            classes_db.create_classes_date=campus.create_classes_date
            classes_db.founder_type=campus.founder_type
            classes_db.founder_name=campus.founder_name
            classes_db.urban_rural_nature=campus.urban_rural_nature
            classes_db.classes_operation_type=campus.classes_operation_type
            classes_db.classes_org_form=campus.classes_org_form
            classes_db.classes_operation_type_lv2=campus.classes_operation_type_lv2
            classes_db.classes_operation_type_lv3=campus.classes_operation_type_lv3
            classes_db.department_unit_number=campus.department_unit_number
            classes_db.sy_zones=campus.sy_zones
            classes_db.historical_evolution=campus.historical_evolution


        classes_db = await self.classes_dao.update_classes(classes_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # campus = orm_model_to_view_model(classes_db, ClassesModel, exclude=[""])
        return classes_db

    async def softdelete_classes(self, classes_id):
        exists_campus = await self.classes_dao.get_classes_by_id(classes_id)
        if not exists_campus:
            raise Exception(f"校区教育信息{classes_id}不存在")
        classes_db = await self.classes_dao.softdelete_classes(exists_campus)
        # campus = orm_model_to_view_model(classes_db, ClassesModel, exclude=[""],)
        return classes_db


    async def get_classes_count(self):
        return await self.classes_dao.get_classes_count()

    async def query_classes_with_page(self, page_request: PageRequest, classes_name=None,
                                              classes_id=None,classes_no=None ):
        paging = await self.classes_dao.query_classes_with_page(classes_name, classes_id,classes_no,
                                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, ClassesModel)
        return paging_result

