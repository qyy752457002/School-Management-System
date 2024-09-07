# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import copy
from typing import List

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.tenant import TenantNotFoundError, TenantAlreadyExistError
from daos.planning_school_dao import PlanningSchoolDAO
from daos.tenant_dao import TenantDAO
from daos.school_dao import SchoolDAO
from models.tenant import Tenant
from rules.common.common_rule import get_org_center_application
from views.models.system import InstitutionType
from views.models.tenant import Tenant as TenantModel
from views.models.extend_params import ExtendParams
from mini_framework.multi_tenant.tenant import Tenant as TenantViewModel


@dataclass_inject
class TenantRule(object):
    tenant_dao: TenantDAO
    school_dao: SchoolDAO
    plannning_school_dao: PlanningSchoolDAO

    async def get_tenant_by_id(self, tenant_id):
        tenant_id=int(tenant_id)
        tenant_db = await self.tenant_dao.get_tenant_by_id(tenant_id)
        # 可选 , exclude=[""]
        tenant = orm_model_to_view_model(tenant_db, TenantModel)
        return tenant
    async def get_tenant_by_code(self, tenant_code):
        tenant_db = await self.tenant_dao.get_tenant_by_code(tenant_code)
        if tenant_db is None:
            # 可能是 区 或者 市的编码的情况
            # school  = await self.school_dao.get_school_by_args(block=tenant_code,planning_school_id =  0)
            school  = await self.school_dao.get_school_by_tenant_code(tenant_code )

        # school_rule= get_injector(SchoolRule)
        #     school  =  school_rule.get_country_edu_institution_by_code(tenant_code)
            if school is None:
                print('未找到区教育局')
                return None
            tenant_db = await self.tenant_dao.get_tenant_by_code(school.school_no)
            if tenant_db is None:
                print('找到区教育局,但不存在于租户表里-租户未激活')
                return None
        tenant = orm_model_to_view_model(tenant_db, TenantViewModel)
        return tenant
    async def get_tenant_by_name(self, tenant_name):
        tenant_db = await self.tenant_dao.get_tenant_by_name(tenant_name)
        # 可选 , exclude=[""]
        tenant = orm_model_to_view_model(tenant_db, TenantModel)
        return tenant

    async def add_tenant(self, tenant: TenantModel):
        exists_tenant = await self.tenant_dao.get_tenant_by_name(
            tenant.tenant_name,tenant)
        if exists_tenant:
            raise TenantAlreadyExistError()
        tenant_db = view_model_to_orm_model(tenant, Tenant,    exclude=["id"])
        tenant_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        tenant_db = await self.tenant_dao.add_tenant(tenant_db)
        tenant = orm_model_to_view_model(tenant_db, TenantModel, exclude=["created_at",'updated_at'])
        return tenant

    async def update_tenant(self, tenant,ctype=1):
        exists_tenant = await self.tenant_dao.get_tenant_by_id(tenant.id)
        if not exists_tenant:
            raise TenantNotFoundError()
        need_update_list = []
        for key, value in tenant.dict().items():
            if value:
                need_update_list.append(key)

        tenant_db = await self.tenant_dao.update_tenant(tenant, *need_update_list)


        # tenant_db = await self.tenant_dao.update_tenant(tenant_db,ctype)
        # 更新不用转换   因为得到的对象不熟全属性
        # tenant = orm_model_to_view_model(tenant_db, TenantModel, exclude=[""])
        return tenant_db

    async def softdelete_tenant(self, tenant_id):
        exists_tenant = await self.tenant_dao.get_tenant_by_id(tenant_id)
        if not exists_tenant:
            raise Exception(f"课程信息{tenant_id}不存在")
        tenant_db = await self.tenant_dao.softdelete_tenant(exists_tenant)
        return tenant_db
    async def softdelete_tenant_by_school_id(self, tenant_id):
        tenant_db = await self.tenant_dao.softdelete_tenant_by_school_id(tenant_id)
        return tenant_db
    async def softdelete_tenant_by_district(self, tenant_id):
        tenant_db = await self.tenant_dao.softdelete_tenant_by_district(tenant_id)
        return tenant_db

    async def get_tenant_count(self):
        return await self.tenant_dao.get_tenant_count()

    async def query_tenant_with_page(self, page_request: PageRequest,school_id=None, tenant_name=None,
                                              tenant_id=None,tenant_no=None ,extobj:ExtendParams=None):
        kdict = {
            "tenant_name": tenant_name,
            "school_id": school_id,
            "tenant_id": tenant_id,
            "tenant_no": tenant_no,
            "school_nature": None,
            "city": extobj.city,
            "district": extobj.county_id,
            "is_deleted":False
        }
        if not kdict["tenant_name"]:
            del kdict["tenant_name"]
        if not kdict["school_id"]:
            del kdict["school_id"]
        if not kdict["tenant_id"]:
            del kdict["tenant_id"]
        if not kdict["tenant_no"]:
            del kdict["tenant_no"]
        if not kdict["city"]:
            del kdict["city"]
        if not kdict["district"]:
            del kdict["district"]
        # 如果有学校ID  读取学校的 二级类型
        if school_id is not None:
            school_info = await self.school_dao.get_school_by_id(school_id)
            if school_info:
                kdict["school_nature"] = school_info.school_category
        print(kdict)

        paging = await self.tenant_dao.query_tenant_with_page(page_request,**kdict
                                                                                )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, TenantModel)
        # convert_snowid_to_strings(paging_result, ["id", "school_id",'grade_id',])
        return paging_result


    async def get_tenant_all(self, filterdict):
        items =  await self.tenant_dao.get_all_tenant(filterdict)
        items = copy.deepcopy(items)
        # for item in items:
            # convert_snowid_in_model(item,["id", "school_id",'grade_id',])
        return items


    async def add_tenant_school(self,school_id,tenant_list:List[TenantModel],obj:ExtendParams=None):
        res=None
        if school_id:
            exists_tenant = await self.tenant_dao.get_tenant_by_school_id(      school_id)
            if exists_tenant:
                raise TenantAlreadyExistError()
        #     自动对list里的课程遍历 针对tenantno去重
        cousrnos= [ ]

        for tenant in tenant_list:
            if tenant.tenant_no in cousrnos:
                print("重复课程",tenant.tenant_no)
                continue
            cousrnos.append(tenant.tenant_no)
            # 扩展参数 放入到视图模型 再转换给orm
            if obj and  obj.county_id:
                tenant.district=obj.county_id
            if obj  and  obj.edu_type:
                tenant.school_type=obj.edu_type
            tenant_db= view_model_to_orm_model(tenant, Tenant, exclude=["id"])
            tenant_db.id = SnowflakeIdGenerator(1, 1).generate_id()

            res = await self.tenant_dao.add_tenant(tenant_db)
        tenant = orm_model_to_view_model(res, TenantModel, exclude=["created_at",'updated_at'])
        # convert_snowid_in_model(tenant, ["id", "school_id",'grade_id',])
        return tenant

    async def sync_tenant_all(self, school_id):
        """市   用 市编号      当前用区号 +行政单位筛选    备用的 产品会定义一个机构编号 其中的第几位标识这个单位是否有管理全区学校的权限
         区     区号
          学校   学校ID
            事业单位
             行政单位
              """
        print(school_id)
        items =  await self.plannning_school_dao.get_planning_school_by_id(school_id)
        tenant_type= 'planning_school'
        if items is None:
            print('学校未找到当前租户')
            items =  await self.school_dao.get_school_by_id(school_id)
            if items is None:
                print('分校未找到当前租户')

                return
            else:
                tenant_type= 'school'
        else:
            pass
            # return
        if tenant_type == 'school':
            # 学校用编号

            code = items.school_no
            description = items.school_name

            pass
        else:
            # 规划校用编号
            code = items.planning_school_no
            description = items.planning_school_name
            pass

        # 不重复插入 租户
        tenant  =  await self.tenant_dao.get_tenant_by_code(code)
        if tenant is not  None:
            return
        # 请求接口  解析放入表里
        res  =await  get_org_center_application(code)
        for value in  res['data']:
            if value['owner']!= code:
                continue

            if tenant_type == 'school' and   items.institution_category not  in [InstitutionType.INSTITUTION,InstitutionType.ADMINISTRATION] :
                # 学校用的是 ID  事业单位用的是区号 school_no
                code = str(items.id)
                pass


            tenant_db = Tenant(
                id=SnowflakeIdGenerator(1, 1).generate_id(),
                tenant_type=  tenant_type,
                status= 'active',
                code=code,
                name=value['name'],
                client_id=value['clientId'],
                description=description,
                # school_id=school_id,
                origin_id=int(school_id),
                client_secret=value['clientSecret'],
                cert_public_key=value['certPublicKey'],
            )
            res_add  = await self.tenant_dao.add_tenant(tenant_db)
            print('保存结果',res_add )

        # for item in items:
        # convert_snowid_in_model(item,["id", "school_id",'grade_id',])
        return items
