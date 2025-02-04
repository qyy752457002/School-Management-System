# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import copy

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.major import MajorAlreadyExistError
from daos.major_dao import MajorDAO
from models.major import Major
from views.common.common_view import convert_snowid_to_strings, convert_snowid_in_model
from views.models.majors import Majors as MajorModel


@dataclass_inject
class MajorRule(object):
    major_dao: MajorDAO

    async def get_major_by_id(self, major_id):
        major_db = await self.major_dao.get_major_by_id(major_id)
        # 可选 , exclude=[""]
        major = orm_model_to_view_model(major_db, MajorModel)
        return major
    async def get_major_by_name(self, major_name):
        major_db = await self.major_dao.get_major_by_name(major_name)
        # 可选 , exclude=[""]
        major = orm_model_to_view_model(major_db, MajorModel)
        return major

    async def add_major(self, major: MajorModel):
        exists_major = await self.major_dao.get_major_by_name(
            major.major_name,major )
        if exists_major:
            raise Exception(f"专业信息{major.major_name}已存在")
        major_db = view_model_to_orm_model(major, Major,    exclude=["id"])
        major_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        major_db = await self.major_dao.add_major(major_db)
        major = orm_model_to_view_model(major_db, MajorModel, exclude=["created_at",'updated_at'])
        convert_snowid_in_model(major,  ["id", "school_id",'institution_id','planning_school_id'])
        return major

    async def add_major_multi(self,school_id,major_list):
        exists_major = await self.major_dao.get_major_by_school_id(      school_id)
        if exists_major:
            raise MajorAlreadyExistError()
        # major_db =  Course(school_id=school_id,major_list=major_list)
        # 定义 视图和model的映射关系
        original_dict_map_view_orm ={"major_no":"major_id"}
        flipped_dict = {v: k for k, v in original_dict_map_view_orm.items()}
        res=None
        if not major_list:
            return {"msg":"操作成功"}
        for major in major_list:
            major_db= view_model_to_orm_model(major, Major, exclude=["id"],other_mapper=original_dict_map_view_orm)
            major_db.school_id=school_id
            major_db.id = SnowflakeIdGenerator(1, 1).generate_id()

            res = await self.major_dao.add_major(major_db)

            # print(major_db.major_list)

        # major_db = await self.major_dao.add_major(major_db)
        major = orm_model_to_view_model(res, MajorModel, exclude=["created_at",'updated_at'],other_mapper=flipped_dict)
        convert_snowid_in_model(major,  ["id", "school_id",'institution_id','planning_school_id'])

        return major

    async def update_major(self, major,ctype=1):
        exists_major = await self.major_dao.get_major_by_id(major.id)
        if not exists_major:
            raise Exception(f"专业信息{major.id}不存在")
        need_update_list = []
        for key, value in major.dict().items():
            if value:
                need_update_list.append(key)

        major_db = await self.major_dao.update_major(major, *need_update_list)


        # major_db = await self.major_dao.update_major(major_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # major = orm_model_to_view_model(major_db, MajorModel, exclude=[""])
        convert_snowid_in_model(major_db,  ["id", "school_id",'institution_id','planning_school_id'])

        return major_db

    async def softdelete_major(self, major_id):
        exists_major = await self.major_dao.get_major_by_id(major_id)
        if not exists_major:
            raise Exception(f"专业信息{major_id}不存在")
        major_db = await self.major_dao.softdelete_major(exists_major)
        major_db=copy.deepcopy(major_db)
        convert_snowid_in_model(major_db,  ["id", "school_id",'institution_id','planning_school_id'])

        return major_db

    async def softdelete_major_by_school_id(self, major_id):
        major_db = await self.major_dao.softdelete_major_by_school_id(major_id)
        return major_db


    async def get_major_count(self):
        return await self.major_dao.get_major_count()

    async def query_major_with_page_param(self, page_request: PageRequest, school_id ):

        paging = await self.major_dao.query_major_with_page_param(page_request,school_id
                                                            )
        # 字段映射的示例写法   , {"hash_password": "password"}
        original_dict_map_view_orm ={"major_no":"major_id"}
        flipped_dict = {v: k for k, v in original_dict_map_view_orm.items()}
        paging_result = PaginatedResponse.from_paging(paging, MajorModel ,other_mapper= flipped_dict)
        convert_snowid_to_strings(paging_result, ["id", "school_id",])

        return paging_result


    async def get_major_all(self, filterdict):
        return await self.major_dao.get_all_major(filterdict)

