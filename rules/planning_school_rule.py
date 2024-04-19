# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from business_exceptions.planning_school import PlanningSchoolNotFoundError
from daos.planning_school_dao import PlanningSchoolDAO
from models.planning_school import PlanningSchool
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus

from views.models.planning_school import PlanningSchoolBaseInfo
from mini_framework.databases.conn_managers.db_manager import db_connection_manager


@dataclass_inject
class PlanningSchoolRule(object):
    planning_school_dao: PlanningSchoolDAO

    async def get_planning_school_by_id(self, planning_school_id):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not planning_school_db:
            raise PlanningSchoolNotFoundError()
        # 可选 , exclude=[""]
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel)
        return planning_school

    async def get_planning_school_by_planning_school_name(self, planning_school_name):
        planning_school_db = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school_name)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school

    async def add_planning_school(self, planning_school: PlanningSchoolModel):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_planning_school_name(
            planning_school.planning_school_name)
        if exists_planning_school:
            raise Exception(f"规划校{planning_school.planning_school_name}已存在")
        planning_school_db = view_model_to_orm_model(planning_school, PlanningSchool,    exclude=["id"])
        planning_school_db.status =  PlanningSchoolStatus.DRAFT.value
        planning_school_db.created_uid = 0
        planning_school_db.updated_uid = 0

        planning_school_db = await self.planning_school_dao.add_planning_school(planning_school_db)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=["created_at",'updated_at'])
        return planning_school

    async def update_planning_school(self, planning_school,ctype=1):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school.id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        if ctype==1:
            planning_school_db = PlanningSchool()
            planning_school_db.id = planning_school.id
            planning_school_db.planning_school_no = planning_school.planning_school_no
            planning_school_db.planning_school_name = planning_school.planning_school_name
            planning_school_db.block = planning_school.block
            planning_school_db.borough = planning_school.borough
            planning_school_db.planning_school_type = planning_school.planning_school_type
            planning_school_db.planning_school_operation_type = planning_school.planning_school_operation_type
            planning_school_db.planning_school_operation_type_lv2 = planning_school.planning_school_operation_type_lv2
            planning_school_db.planning_school_operation_type_lv3 = planning_school.planning_school_operation_type_lv3
            planning_school_db.planning_school_org_type = planning_school.planning_school_org_type
            planning_school_db.planning_school_level = planning_school.planning_school_level
        else:
            planning_school_db = PlanningSchool()
            planning_school_db.id = planning_school.id
            planning_school_db.planning_school_name=planning_school.planning_school_name
            planning_school_db.planning_school_short_name=planning_school.planning_school_short_name
            planning_school_db.planning_school_code=planning_school.planning_school_code
            planning_school_db.create_planning_school_date=planning_school.create_planning_school_date
            planning_school_db.founder_type=planning_school.founder_type
            planning_school_db.founder_name=planning_school.founder_name
            planning_school_db.urban_rural_nature=planning_school.urban_rural_nature
            planning_school_db.planning_school_operation_type=planning_school.planning_school_operation_type
            planning_school_db.planning_school_org_form=planning_school.planning_school_org_form
            planning_school_db.planning_school_operation_type_lv2=planning_school.planning_school_operation_type_lv2
            planning_school_db.planning_school_operation_type_lv3=planning_school.planning_school_operation_type_lv3
            planning_school_db.department_unit_number=planning_school.department_unit_number
            planning_school_db.sy_zones=planning_school.sy_zones
            planning_school_db.historical_evolution=planning_school.historical_evolution


        planning_school_db = await self.planning_school_dao.update_planning_school(planning_school_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""])
        return planning_school_db

    async def delete_planning_school(self, planning_school_id):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        planning_school_db = await self.planning_school_dao.delete_planning_school(exists_planning_school)
        planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        return planning_school

    async def softdelete_planning_school(self, planning_school_id):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        planning_school_db = await self.planning_school_dao.softdelete_planning_school(exists_planning_school)
        # planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        return planning_school_db

    async def get_all_planning_schools(self):
        return await self.planning_school_dao.get_all_planning_schools()

    async def get_planning_school_count(self):
        return await self.planning_school_dao.get_planning_school_count()

    async def query_planning_school_with_page(self, page_request: PageRequest,  planning_school_name,planning_school_no,planning_school_code,
                                              block,planning_school_level,borough,status ,founder_type,
                                              founder_type_lv2,
                                              founder_type_lv3 ):
        paging = await self.planning_school_dao.query_planning_school_with_page(  page_request, planning_school_name,planning_school_no,planning_school_code,
                                                                                  block,planning_school_level,borough,status,founder_type,
                                                                                  founder_type_lv2,
                                                                                  founder_type_lv3 )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, PlanningSchoolModel)
        return paging_result


    async def update_planning_school_status(self, planning_school_id, status):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school_id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        # 判断运来的状态 进行后续的更新
        if status== PlanningSchoolStatus.NORMAL.value and exists_planning_school.status== PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_planning_school.status= PlanningSchoolStatus.NORMAL.value
        elif status== PlanningSchoolStatus.CLOSED.value and exists_planning_school.status== PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_planning_school.status= PlanningSchoolStatus.CLOSED.value
        else:
            # exists_planning_school.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"规划校当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')
        #
        # for key, value in exists_planning_school.dict().items():
        #     if value:
        #         need_update_list.append(key)


        print(exists_planning_school.status,2222222)
        planning_school_db = await self.planning_school_dao.update_planning_school_byargs(exists_planning_school,*need_update_list)
        # planning_school = orm_model_to_view_model(planning_school_db, PlanningSchoolModel, exclude=[""],)
        return planning_school_db



    async def update_planning_school_byargs(self, planning_school,ctype=1):
        exists_planning_school = await self.planning_school_dao.get_planning_school_by_id(planning_school.id)
        if not exists_planning_school:
            raise PlanningSchoolNotFoundError()
        need_update_list = []
        for key, value in planning_school.dict().items():
            if value:
                need_update_list.append(key)

        if exists_planning_school.status== PlanningSchoolStatus.DRAFT.value:
            planning_school.status= PlanningSchoolStatus.OPENING.value
        else:
            pass

        planning_school_db = await self.planning_school_dao.update_planning_school_byargs(planning_school, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # planning_school = orm_model_to_view_model(planning_school_db, SchoolModel, exclude=[""])
        return planning_school_db




    async def query_planning_schools(self,planning_school_name):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(PlanningSchool).where(PlanningSchool.planning_school_name.like(f'{planning_school_name}%') ))
        res= result.scalars().all()
        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, PlanningSchoolModel)
            # account = PlanningSchool(school_id=row.school_id,
            #                  grade_no=row.grade_no,
            #                  grade_name=row.grade_name,
            #                  grade_alias=row.grade_alias,
            #                  description=row.description)
            lst.append(planning_school)
        return lst
        # return await self.planning_school_dao.get_all_planning_schools()
