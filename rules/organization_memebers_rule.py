# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.utils.logging import logger
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from sqlalchemy import select

from business_exceptions.organization import OrganizationMemberExistError, OrganizationMemberNotFoundError
from daos.organization_dao import OrganizationDAO
from daos.organization_members_dao import OrganizationMembersDAO
from daos.school_dao import SchoolDAO
from daos.teachers_dao import TeachersDao
from models.organization import Organization as OrganizationModel
from models.organization_members import OrganizationMembers as OrganizationMembersModel
from rules.common.common_rule import send_orgcenter_request
# from daos.organization_members_dao import CampusDAO
# from daos.organization_members_dao import OrganizationDAO
# from daos.organization_members_members_dao import OrganizationMembersDAO
# from models.organization import Campus
from rules.organization_rule import OrganizationRule
from views.common.common_view import convert_snowid_to_strings, convert_snowid_in_model
from views.models.organization import Organization, OrganizationMembers, OrganizationMembersSearchRes
# from views.models.organization import CampusBaseInfo
from views.models.planning_school import PlanningSchoolStatus
from views.models.teachers import EducateUserModel


# from views.models.organization import Campus as Organization
@dataclass_inject
class OrganizationMembersRule(object):
    organization_members_dao: OrganizationMembersDAO
    organization_dao: OrganizationDAO
    school_dao: SchoolDAO
    teacher_dao: TeachersDao

    async def get_organization_members_by_id(self, organization_members_id, extra_model=None):
        organization_members_db = await self.organization_members_dao.get_organization_members_by_id(
            organization_members_id)
        # 可选 , exclude=[""]
        if extra_model:
            # school = orm_model_to_view_model(school_db, extra_model)
            organization = orm_model_to_view_model(organization_members_db, extra_model)

        else:
            organization = orm_model_to_view_model(organization_members_db, Organization)
        return organization

    async def get_organization_members_by_organization_members_name(self, organization_members_name):
        organization_members_db = await self.organization_members_dao.get_organization_members_by_organization_members_name(
            organization_members_name)
        organization = orm_model_to_view_model(organization_members_db, Organization, exclude=[""])
        return organization

    # todo 增加 对 部门计数的更新
    async def add_organization_members(self, organization_members: OrganizationMembers):
        # 去重和 新增插入    有可能重复  手动处理去重
        logger.debug("增加组织成员", organization_members)
        print("add_organization_members", organization_members)
        exists_organization_members = await self.organization_members_dao.get_organization_members_by_param(
            organization_members)
        if exists_organization_members:
            raise OrganizationMemberExistError()
        organization_members_db = view_model_to_orm_model(organization_members, OrganizationMembersModel,
                                                          exclude=["id"])
        organization_members_db.created_uid = 0
        organization_members_db.updated_uid = 0
        organization_members_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        organization_members_db = await self.organization_members_dao.add_organization_members(organization_members_db)
        organization_members_db_res = orm_model_to_view_model(organization_members_db, OrganizationMembers,
                                                              exclude=["created_at", 'updated_at'], other_mapper={})
        # 更新部门成员的计数
        org_rule = get_injector(OrganizationRule)
        cnt = await self.get_organization_members_count(organization_members.org_id)

        orginfo = await self.organization_dao.get_organization_by_id(organization_members_db.org_id)
        if orginfo:
            orginfo_vm = orm_model_to_view_model(orginfo, Organization, exclude=["created_at", 'updated_at'],
                                                 other_mapper={})

            orginfo_vm.member_cnt = cnt
            await org_rule.update_organization(orginfo_vm)

        convert_snowid_in_model(organization_members_db_res, ["id", "school_id", 'parent_id', 'teacher_id', 'org_id'])
        # todo 部门成员 对接到组织中心  兼容 教师和 普通添加
        # 管理员 对接
        try:
            res_admin = await self.send_admin_to_org_center(organization_members_db, )
        except Exception as e:
            logger.error(e)
            print('部门成员 对接到组织中心 异常', e)

        return organization_members_db_res

    async def update_organization_members(self, organization, ):
        # 默认 改 支持通过ID来修改或者通过教师ID 组织ID来修改
        if organization.id:

            exists_organization_members = await self.organization_members_dao.get_organization_members_by_id(
                organization.id)
        else:
            exists_organization_members = await self.organization_members_dao.get_organization_members_by_param(
                organization)
            if exists_organization_members:
                organization.id = exists_organization_members.id

        if not exists_organization_members:
            raise OrganizationMemberNotFoundError()
        organization_members_db = view_model_to_orm_model(organization, OrganizationMembersModel, exclude=[])
        need_update_list = []
        # 自动判断哪些字段需要更新
        for key, value in organization.dict().items():
            if value:
                need_update_list.append(key)

        organization_members_db = await self.organization_members_dao.update_organization_members(
            organization_members_db, *need_update_list)
        print(organization_members_db, 999)
        convert_snowid_in_model(organization_members_db, ["id", "school_id", 'parent_id', 'teacher_id', 'org_id'])

        return organization_members_db

    async def update_organization_members_by_teacher_id(self, organization: OrganizationMembers, ):
        # 多个部门都删掉  再插入最新

        exists_organization_members = await self.organization_members_dao.delete_organization_members_by_teacher_id(
            organization.teacher_id)

        organization_members_db = view_model_to_orm_model(organization, OrganizationMembersModel, )
        # school_db.status =  PlanningSchoolStatus.DRAFT.value
        organization_members_db.created_uid = 0
        organization_members_db.updated_uid = 0

        organization_members_db = await self.organization_members_dao.add_organization_members(organization_members_db)
        organization = orm_model_to_view_model(organization_members_db, Organization,
                                               exclude=["created_at", 'updated_at'])
        return organization

    async def delete_organization_members(self, organization_members_id):
        exists_organization = await self.organization_members_dao.get_organization_members_by_id(
            organization_members_id, True)
        if not exists_organization:
            raise OrganizationMemberNotFoundError()
        organization_members_db = await self.organization_members_dao.delete_organization_members(exists_organization)
        organization = orm_model_to_view_model(organization_members_db, Organization, exclude=[""], )
        convert_snowid_in_model(organization, ["id", "school_id", 'parent_id', 'teacher_id', 'org_id'])

        return organization

    async def softdelete_organization_members(self, organization_members_id):
        exists_organization = await self.organization_members_dao.get_organization_members_by_id(
            organization_members_id)
        if not exists_organization:
            raise Exception(f"{organization_members_id}不存在")
        organization_members_db = await self.organization_members_dao.softdelete_organization_members(
            exists_organization)
        # organization = orm_model_to_view_model(organization_members_db, Organization, exclude=[""],)
        return organization_members_db

    async def get_all_organization_memberss(self):
        return await self.organization_members_dao.get_all_organization_memberss()

    async def get_organization_members_count(self, org_id):
        return await self.organization_members_dao.get_organization_members_count(org_id)

    async def query_organization_members_with_page(self, page_request: PageRequest, parent_id, school_id, teacher_name,
                                                   teacher_no, mobile, birthday, org_ids):
        parent_id_lv2 = []
        if parent_id:
            #   参照 举办者类型   自动查出 下一级的 23 级
            res = await self.query_organization_members(parent_id)
            for item in res:
                parent_id_lv2.append(item.id)

            pass
        if not parent_id_lv2:
            # parent_id_lv2= [int(parent_id)]
            pass
        if org_ids and isinstance(org_ids, str):
            org_ids = org_ids.split(',')
            int_list = [int(i) for i in org_ids]
            parent_id_lv2 = parent_id_lv2 + int_list

        paging = await self.organization_members_dao.query_organization_members_with_page(page_request, parent_id_lv2,
                                                                                          school_id, teacher_name,
                                                                                          teacher_no, mobile, birthday
                                                                                          )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, OrganizationMembersSearchRes, other_mapper={
            "teacher_name": "member_name",
            "teacher_date_of_birth": "birthday",
            "teacher_gender": "gender",
            # "teacher_mobile": "updated_at",
            "teacher_id_type": "card_type",
            # "teacher_identity": "updated_at",
            "teacher_id_number": "card_number",
        })
        convert_snowid_to_strings(paging_result, ["id", "school_id", 'parent_id', 'teacher_id', 'org_id'])
        return paging_result

    async def update_organization_members_status(self, organization_members_id, status, action=None):
        exists_organization = await self.organization_members_dao.get_organization_members_by_id(
            organization_members_id)
        if not exists_organization:
            raise Exception(f"学校{organization_members_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status == PlanningSchoolStatus.NORMAL.value and exists_organization.status == PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_organization.status = PlanningSchoolStatus.NORMAL.value
        elif status == PlanningSchoolStatus.CLOSED.value and exists_organization.status == PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_organization.status = PlanningSchoolStatus.CLOSED.value
        else:
            # exists_organization.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"学校当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')

        # print(exists_organization.status,2222222)
        organization_members_db = await self.organization_members_dao.update_organization_members_byargs(
            exists_organization, *need_update_list)

        # organization_members_daodb = await self.organization_members_dao.update_organization_members_daostatus(exists_organization,status)
        # school = orm_model_to_view_model(organization_members_daodb, SchoolModel, exclude=[""],)
        return organization_members_db

    async def query_organization_members(self, parent_id, ):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(OrganizationModel).where(OrganizationModel.parent_id == int(parent_id)))
        res = result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, Organization)
            convert_snowid_in_model(planning_school)

            lst.append(planning_school)
        return lst

    async def send_admin_to_org_center(self, organization_member: OrganizationMembersModel, ):
        orginfo = await self.organization_dao.get_organization_by_id(organization_member.org_id)
        school = await self.school_dao.get_school_by_id(orginfo.school_id)
        teacher = await self.teacher_dao.get_teachers_by_id(organization_member.teacher_id)
        # data_dict = to_dict(teacher_db)
        # print(data_dict)
        dict_data = EducateUserModel(**organization_member.__dict__,
                                     currentUnit=school.school_name,
                                     createdTime=organization_member.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     updatedTime=organization_member.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                                     name=teacher.teacher_name,
                                     owner=school.school_no,
                                     userCode=teacher.teacher_id_number,
                                     phoneNumber=teacher.mobile,
                                     # 部门group 的显示名字
                                     # departmentNames=data_org['displayName'],
                                     departmentNames=orginfo.org_name,
                                     # "name":
                                     # 部门group的name
                                     # departmentId=data_org['name'],
                                     departmentId="基础信息管理系统",
                                     realName=teacher.teacher_name
                                     )
        dict_data = dict_data.__dict__
        # params_data = JsonUtils.dict_to_json_str(dict_data)
        api_name = '/api/add-educate-user'
        # 字典参数
        datadict = dict_data
        print(datadict, '参数')
        response = await send_orgcenter_request(api_name, datadict, 'post', False)
        print('  管理员 对接 ', response, )
        try:
            # print(response)
            return response
        except Exception as e:
            print(e)
            raise e
            return response
        return None
