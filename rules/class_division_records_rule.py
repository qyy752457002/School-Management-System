# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.class_division_records_dao import ClassDivisionRecordsDAO
from models.class_division_records import ClassDivisionRecords
from views.models.class_division_records import ClassDivisionRecords as ClassDivisionRecordsModel
from views.models.class_division_records import ClassDivisionRecordsSearchRes

@dataclass_inject
class ClassDivisionRecordsRule(object):
    class_division_records_dao: ClassDivisionRecordsDAO

    async def get_class_division_records_by_id(self, class_division_records_id):
        class_division_records_db = await self.class_division_records_dao.get_class_division_records_by_id(class_division_records_id)
        # 可选 , exclude=[""]
        classes = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel)
        return classes

    async def add_classes(self, classes: ClassDivisionRecordsModel):
        exists_classes = await self.class_division_records_dao.get_class_division_records_by_class_division_records_name(
            classes.class_name, classes.school_id)
        if exists_classes:
            raise Exception(f"班级信息{classes.class_name}已存在")
        class_division_records_db = view_model_to_orm_model(classes, ClassDivisionRecords, exclude=["id"])

        class_division_records_db = await self.class_division_records_dao.add_classes(class_division_records_db)
        classes = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel, exclude=["created_at", 'updated_at'])
        return classes

    async def update_classes(self, classes, ctype=1):
        exists_classes = await self.class_division_records_dao.get_class_division_records_by_id(classes.id)
        if not exists_classes:
            raise Exception(f"班级信息{classes.id}不存在")
        need_update_list = []
        for key, value in classes.dict().items():
            if value:
                need_update_list.append(key)

        class_division_records_db = await self.class_division_records_dao.update_class_division_records_byargs(classes, *need_update_list)

        # class_division_records_db = await self.class_division_records_dao.update_classes(class_division_records_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # classes = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel, exclude=[""])
        return class_division_records_db

    async def softdelete_classes(self, class_division_records_id):
        exists_classes = await self.class_division_records_dao.get_class_division_records_by_id(class_division_records_id)
        if not exists_classes:
            raise Exception(f"班级信息{class_division_records_id}不存在")
        class_division_records_db = await self.class_division_records_dao.delete_class_division_records(exists_classes)
        # classes = orm_model_to_view_model(class_division_records_db, ClassDivisionRecordsModel, exclude=[""],)
        return class_division_records_db

    async def get_class_division_records_count(self):
        return await self.class_division_records_dao.get_class_division_records_count()

    async def query_class_division_records_with_page(self, page_request: PageRequest, borough, block, school_id, grade_id, class_name):
        paging = await self.class_division_records_dao.query_class_division_records_with_page(borough, block, school_id, grade_id, class_name,
                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"} ClassDivisionRecordsSearchRes
        print(paging)
        paging_result = PaginatedResponse.from_paging(paging, ClassDivisionRecordsSearchRes,other_mapper={"school_name": "school_name",})
        return paging_result
