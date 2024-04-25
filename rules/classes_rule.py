# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.class_dao import ClassesDAO
from models.classes import Classes
from views.models.classes import Classes as ClassesModel
from views.models.classes import ClassesSearchRes

@dataclass_inject
class ClassesRule(object):
    classes_dao: ClassesDAO

    async def get_classes_by_id(self, classes_id):
        classes_db = await self.classes_dao.get_classes_by_id(classes_id)
        # 可选 , exclude=[""]
        classes = orm_model_to_view_model(classes_db, ClassesModel)
        return classes

    async def add_classes(self, classes: ClassesModel):
        exists_classes = await self.classes_dao.get_classes_by_classes_name(
            classes.class_name)
        if exists_classes:
            raise Exception(f"班级信息{classes.class_name}已存在")
        classes_db = view_model_to_orm_model(classes, Classes, exclude=["id"])

        classes_db = await self.classes_dao.add_classes(classes_db)
        classes = orm_model_to_view_model(classes_db, ClassesModel, exclude=["created_at", 'updated_at'])
        return classes

    async def update_classes(self, classes, ctype=1):
        exists_classes = await self.classes_dao.get_classes_by_id(classes.id)
        if not exists_classes:
            raise Exception(f"班级信息{classes.id}不存在")
        need_update_list = []
        for key, value in classes.dict().items():
            if value:
                need_update_list.append(key)

        classes_db = await self.classes_dao.update_classes_byargs(classes, *need_update_list)

        # classes_db = await self.classes_dao.update_classes(classes_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # classes = orm_model_to_view_model(classes_db, ClassesModel, exclude=[""])
        return classes_db

    async def softdelete_classes(self, classes_id):
        exists_classes = await self.classes_dao.get_classes_by_id(classes_id)
        if not exists_classes:
            raise Exception(f"班级信息{classes_id}不存在")
        classes_db = await self.classes_dao.softdelete_classes(exists_classes)
        # classes = orm_model_to_view_model(classes_db, ClassesModel, exclude=[""],)
        return classes_db

    async def get_classes_count(self):
        return await self.classes_dao.get_classes_count()

    async def query_classes_with_page(self, page_request: PageRequest, borough, block, school_id, grade_id, class_name):
        paging = await self.classes_dao.query_classes_with_page(borough, block, school_id, grade_id, class_name,
                                                                page_request)
        # 字段映射的示例写法   , {"hash_password": "password"} ClassesSearchRes
        print(paging)
        paging_result = PaginatedResponse.from_paging(paging, ClassesSearchRes)
        return paging_result
