# from mini_framework.databases.entities.toolkit import orm_model_to_view_model
import copy
from datetime import date, datetime

from mini_framework.databases.conn_managers.db_manager import db_connection_manager
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from mini_framework.design_patterns.depend_inject import dataclass_inject, get_injector
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from sqlalchemy import select

from business_exceptions.organization import OrganizationNotFoundError, OrganizationExistError
from business_exceptions.school import SchoolNotFoundError
# from daos.organization_dao import CampusDAO
from daos.organization_dao import OrganizationDAO
# from models.organization import Campus
from rules.enum_value_rule import EnumValueRule
from views.common.common_view import convert_snowid_to_strings, convert_snowid_in_model
from views.models.organization import Organization
# from views.models.organization import Campus as Organization

# from views.models.organization import CampusBaseInfo
from views.models.planning_school import PlanningSchoolStatus
from views.models.school import School as SchoolModel
from models.organization import Organization as OrganizationModel
@dataclass_inject
class OrganizationRule(object):
    organization_dao: OrganizationDAO

    async def get_organization_by_id(self, organization_id,extra_model=None):
        organization_db = await self.organization_dao.get_organization_by_id(organization_id)
        # 可选 , exclude=[""]
        if extra_model:
            # school = orm_model_to_view_model(school_db, extra_model)
            organization = orm_model_to_view_model(organization_db, extra_model)

        else:
            organization = orm_model_to_view_model(organization_db, Organization)
        return organization

    async def get_organization_by_organization_name(self, organization_name):
        organization_db = await self.organization_dao.get_organization_by_organization_name(
            organization_name)
        organization = orm_model_to_view_model(organization_db, Organization, exclude=[""])
        return organization

    async def add_organization(self, organization: Organization):
        exists_organization = await self.organization_dao.get_organization_by_name(
            organization.org_name,organization)
        if exists_organization:
            raise OrganizationExistError()
        #  other_mapper={"password": "hash_password"},
        #                                              exclude=["first_name", "last_name"]
        organization_db = view_model_to_orm_model(organization, OrganizationModel,    exclude=["id"])
        # school_db.status =  PlanningSchoolStatus.DRAFT.value
        # 只有2步  故新增几位开设中 
        organization_db.created_uid = 0
        organization_db.updated_uid = 0
        organization_db.id = SnowflakeIdGenerator(1, 1).generate_id()

        organization_db = await self.organization_dao.add_organization(organization_db)
        organization = orm_model_to_view_model(organization_db, Organization, exclude=["created_at",'updated_at'])
        convert_snowid_in_model(organization, ["id", "school_id",'parent_id',])
        # todo 发送组织中心
        await self.send_org_to_org_center(organization)
        return organization

    async def update_organization(self, organization,):
        # 默认 改
        exists_organization = await self.organization_dao.get_organization_by_id(organization.id)
        if not exists_organization:
            raise  OrganizationNotFoundError()
        organization_db= view_model_to_orm_model(organization, OrganizationModel, exclude=[])
        need_update_list = []
        # 自动判断哪些字段需要更新
        for key, value in organization.dict().items():
            if value:
                need_update_list.append(key)


        organization_db = await self.organization_dao.update_organization(organization_db,*need_update_list)
        print(organization_db,999)
        convert_snowid_in_model(organization_db, ["id", "school_id",'parent_id',])

        return organization_db

    async def update_organization_byargs(self, organization,ctype=1):
        exists_organization = await self.organization_dao.get_organization_by_id(organization.id)
        if not exists_organization:
            raise  OrganizationNotFoundError()
        # if exists_organization.status== PlanningSchoolStatus.DRAFT.value:
        #     exists_organization.status= PlanningSchoolStatus.OPENING.value
        #     organization.status= PlanningSchoolStatus.OPENING.value
        # else:
        #     pass
        need_update_list = []

        for key, value in organization.dict().items():
            if value:
                need_update_list.append(key)

        organization_db = await self.organization_dao.update_organization_byargs(organization, *need_update_list)

        # 更新不用转换   因为得到的对象不熟全属性
        # organization = orm_model_to_view_model(organization_db, Organization, exclude=[""])
        return organization_db

    async def delete_organization(self, organization_id):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id,True)
        if not exists_organization:
            raise OrganizationNotFoundError()
        top_id = exists_organization.parent_id
        organization_db = await self.organization_dao.delete_organization(exists_organization)
        organization = orm_model_to_view_model(organization_db, Organization, exclude=[""],)
        # 查询下层的部门
        if organization_id:
            parent_id_lv2 = await self.organization_dao.get_child_organization_ids([ organization_id])
            parent_id_lv3 = await self.organization_dao.get_child_organization_ids(parent_id_lv2)
            await self.organization_dao.delete_organization_by_ids(parent_id_lv3+parent_id_lv2)
            # organization_db = await self.organization_dao.softdelete_organization(exists_organization)
            pass
        convert_snowid_in_model(organization, ["id", "school_id",'parent_id',])

        return organization

    async def softdelete_organization(self, organization_id):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id)
        if not exists_organization:
            raise Exception(f"{organization_id}不存在")
        organization_db = await self.organization_dao.softdelete_organization(exists_organization)
        # organization = orm_model_to_view_model(organization_db, Organization, exclude=[""],)
        return organization_db

    async def get_all_organizations(self):
        return await self.organization_dao.get_all_organizations()

    async def get_organization_count(self):
        return await self.organization_dao.get_organization_count()

    async def query_organization_with_page(self, page_request: PageRequest,   parent_id , school_id ):
        parent_id_lv2=[]
        if parent_id:
            if int(parent_id) >0:
                parent_id_lv2.append(int(parent_id))
                #
                # # todo  参照 举办者类型   自动查出 23 级
                # res= await self.query_organization( parent_id)
                # for item in res:
                #     parent_id_lv2.append(item.id)
                #
                # pass
            else:
                parent_id_lv2.append(int(parent_id))

        paging = await self.organization_dao.query_organization_with_page(page_request,  parent_id_lv2 , school_id
                                                              )
        # 字段映射的示例写法   , {"hash_password": "password"}
        paging_result = PaginatedResponse.from_paging(paging, Organization)
        convert_snowid_to_strings(paging_result, ["id", "school_id",'parent_id'])
        return paging_result



    async def update_organization_status(self, organization_id, status,action=None):
        exists_organization = await self.organization_dao.get_organization_by_id(organization_id)
        if not exists_organization:
            raise Exception(f"学校{organization_id}不存在")
        # 判断运来的状态 进行后续的更新
        if status== PlanningSchoolStatus.NORMAL.value and exists_organization.status== PlanningSchoolStatus.OPENING.value:
            # 开办
            exists_organization.status= PlanningSchoolStatus.NORMAL.value
        elif status== PlanningSchoolStatus.CLOSED.value and exists_organization.status== PlanningSchoolStatus.NORMAL.value:
            # 关闭
            exists_organization.status= PlanningSchoolStatus.CLOSED.value
        else:
            # exists_organization.status= PlanningSchoolStatus.OPENING.value
            raise Exception(f"学校当前状态不支持您的操作")

        need_update_list = []
        need_update_list.append('status')

        # print(exists_organization.status,2222222)
        organization_db = await self.organization_dao.update_organization_byargs(exists_organization,*need_update_list)


        # organization_daodb = await self.organization_dao.update_organization_daostatus(exists_organization,status)
        # school = orm_model_to_view_model(organization_daodb, SchoolModel, exclude=[""],)
        return organization_db



    async def query_organization(self,parent_id,):

        session = await db_connection_manager.get_async_session("default", True)
        result = await session.execute(select(OrganizationModel).where(OrganizationModel.parent_id == parent_id  ))
        res= result.scalars().all()

        lst = []
        for row in res:
            planning_school = orm_model_to_view_model(row, Organization)
            convert_snowid_in_model(planning_school)

            lst.append(planning_school)
        return lst

    async def increment_organization_member_cnt(self, organization_id,cnt):
        #

        exists_organization_members = await self.organization_dao.update_organization_increment_member_cnt( OrganizationModel(id= int(organization_id), ))

        return organization_id
    async def send_org_to_org_center(self,exists_planning_school_origin):
        exists_planning_school= copy.deepcopy(exists_planning_school_origin)
        if isinstance(exists_planning_school.updated_at, (date, datetime)):
            exists_planning_school.updated_at =exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer


        # planning_school_communication = await self.school_communication_dao.get_school_communication_by_school_id(exists_planning_school.id)
        # cn_exists_planning_school = await self.convert_school_to_export_format(exists_planning_school )
        dict_data = {'administrativeDivisionCity':  '', 'administrativeDivisionCounty': exists_planning_school.block, 'administrativeDivisionProvince':   '', 'createdTime':  exists_planning_school.create_school_date, 'departmentObjs': [{'children': [{'children': [], 'contactEmail': 'x.vjxkswbr@qq.com', 'createdTime': '1987-03-23 02:53:35', 'displayName': '七比什己', 'educateUnit': 'consectetur ipsum sit', 'educateUnitObj': {}, 'isDeleted': False, 'isEnabled': True, 'isTopGroup': False, 'key': 'ipsum non adipisicing', 'manager': 'sed officia', 'name': '两状住法国', 'newCode': '71', 'newType': 'aliquip', 'owner': 'pariatur mollit', 'parentId': '96', 'parentName': '许什件究', 'tags': ['in'], 'title': '始然省非验改', 'type': 'mollit aliquip dolor nostrud', 'updatedTime': '2004-03-21 04:34:58', 'users': [{'accessKey': 'commodo ipsum consectetur irure', 'accessSecret': 'eu est', 'accountStatus': 'pariatur elit irure Ut dolor', 'address': ['甘肃省绵阳市镇雄县'], 'adfs': 'occaecat do eiusmod Duis cillum', 'affiliation': 'voluptate cillum ea', 'alipay': 'non laboris sint in', 'amazon': 'in dolore', 'apple': 'cupidatat qui', 'auth0': 'ullamco sint enim eu pariatur', 'avatar': 'http://dummyimage.com/100x100', 'avatarType': 'http://dummyimage.com/100x100', 'azuread': 'velit deserunt sunt', 'baidu': '9', 'battlenet': 'mollit enim nisi fugiat eiusmod', 'bilibili': 'velit', 'bio': 'ut in dolore dolor veniam', 'birthday': '1979-06-03', 'bitbucket': 'cillum aliquip labore', 'box': 'aliqua', 'casdoor': 'minim aliqua ad culpa', 'cloudfoundry': 'irure cillum minim incididunt est', 'countryCode': '25', 'createdIp': '232.66.103.13', 'createdTime': '1993-03-24 04:52:50', 'custom': 'Excepteur aliqua quis', 'dailymotion': 'eu dolore', 'deezer': 'in in laborum', 'digitalocean': 'Ut ullamco reprehenderit quis sit', 'dingtalk': 'sint aliqua laborum Lorem proident', 'discord': 'occaecat Ut culpa', 'displayName': '至空再指公千', 'douyin': 'Excepteur tempor amet', 'dropbox': 'incididunt aliquip sunt minim anim', 'educateUser': {'avatar': 'http://dummyimage.com/100x100', 'birthDate': '1983-07-30', 'createdTime': '1984-03-28 16:50:03', 'currentUnit': 'ex adipisicing', 'departmentId': '14', 'departmentNames': '员来何现层少学', 'email': 'v.jkr@qq.com', 'gender': '男', 'idCardNumber': '39', 'idCardType': '43', 'identity': '54', 'identityNames': '史也术法', 'identityType': '26', 'identityTypeNames': '放是据其', 'mainUnitName': '低是据角关次具', 'name': '细度战公往它联', 'owner': 'mollit non ad', 'phoneNumber': '69', 'realName': '东委员三高', 'sourceApp': 'aliqua anim ullamco', 'updatedTime': '2015-06-23 06:15:52', 'userCode': '55', 'userId': '49', 'userStatus': 'nisi Ut id dolor'}, 'education': 'Lorem dolor eiusmod velit', 'email': 'p.lwnuavib@qq.com', 'emailVerified': False, 'eveonline': 'non cupidatat Excepteur fugiat in', 'externalId': '51', 'facebook': 'ex', 'firstName': '问选相增养', 'fitbit': 'proident Lorem nulla', 'gender': '女', 'gitea': 'laboris anim fugiat', 'gitee': 'ullamco ex incididunt fugiat consectetur', 'github': 'sed', 'gitlab': 'in sit amet velit', 'google': 'nulla', 'groups': ['incididunt est ex quis'], 'hash': 'non tempor nulla', 'heroku': 'reprehenderit cillum culpa consequat elit', 'homepage': 'anim deserunt sint occaecat et', 'id': '14', 'idCard': '36', 'idCardType': '21', 'influxcloud': 'ex non amet id in', 'infoflow': 'in deserunt', 'instagram': 'labore deserunt dolore', 'intercom': 'aute dolore ipsum', 'isAdmin': False, 'isDefaultAvatar': True, 'isDeleted': True, 'isForbidden': False, 'isOnline': False, 'kakao': 'nulla incididunt ea in magna', 'karma': 57, 'language': 'veniam qui ea et in', 'lark': 'in reprehenderit incididunt in', 'lastName': '此温就置', 'lastSigninIp': '26.197.84.194', 'lastSigninTime': '1991-08-01 11:33:04', 'lastSigninWrongTime': '1984-01-13 17:13:58', 'lastfm': 'tempor ea cupidatat id eu', 'ldap': 'sunt in laboris in Ut', 'line': 'cupidatat ullamco voluptate et', 'linkedin': 'non minim deserunt officia', 'location': 'irure', 'mailru': 'u.ysh@qq.com', 'managedAccounts': [{'application': 'labore est occaecat', 'password': 'est pariatur qui ullamco', 'signinUrl': 'http://eykhvcw.中国/pevksv', 'username': '何磊'}], 'meetup': 'proident', 'metamask': 'aliquip', 'mfaEmailEnabled': True, 'mfaPhoneEnabled': True, 'microsoftonline': 'proident est voluptate occaecat', 'multiFactorAuths': [{'countryCode': '68', 'enabled': False, 'isPreferred': False, 'mfaType': 'Excepteur sunt', 'recoveryCodes': ['82'], 'secret': 'ea ut dolor dolore', 'url': 'http://sdywy.ke/kjpvdlh'}], 'name': '段经备青论', 'naver': 'occaecat', 'nextcloud': 'incididunt cillum', 'okta': 'sed laboris laborum Ut culpa', 'onedrive': 'dolore', 'orgObj': {'accountItems': [{'modifyRule': 'non id exercitation ad', 'name': '究种少万图界', 'viewRule': 'pariatur amet qui ut elit', 'visible': True}], 'accountQuantity': '80', 'countryCodes': ['46'], 'createdTime': '1992-04-21 08:31:34', 'defaultApplication': 'cupidatat ullamco', 'defaultAvatar': 'http://dummyimage.com/100x100', 'defaultPassword': 'culpa officia in', 'displayName': '性任入般变主', 'educateUnits': [{'administrativeDivisionCity': '张家口市', 'administrativeDivisionCounty': 'labore do sed occaecat enim', 'administrativeDivisionProvince': '内蒙古自治区', 'createdTime': '1971-02-21 09:19:05', 'departmentObjs': [], 'locationAddress': planning_school_communication.detailed_address, 'locationCity':  '', 'locationCounty': 'consequat', 'locationProvince':planning_school_communication.loc_area_pro, 'owner': 'deserunt sunt sint id', 'unitCode':  exists_planning_school.school_no , 'unitId': '', 'unitName': exists_planning_school.school_name, 'unitType':exists_planning_school.institution_category, 'updatedTime':  exists_planning_school.updated_at}], 'enableSoftDeletion': True, 'favicon': 'http://dummyimage.com/100x100', 'initScore': 34, 'isProfilePublic': False, 'languages': ['laboris'], 'masterPassword': 'non', 'mfaItems': [{'name': '会力般其气', 'rule': 'in officia minim dolor'}], 'name': '花再一', 'orgType': 'officia', 'overview': 'eu aliqua minim ea', 'owner': 'eiusmod esse dolore amet', 'passwordOptions': ['aute nulla magna tempor in'], 'passwordSalt': 'eiusmod cillum sint incididunt', 'passwordType': 'dolor adipisicing Duis', 'status': 'voluptate deserunt', 'tags': ['proident dolor'], 'themeData': {'borderRadius': 52, 'colorPrimary': 'non', 'isCompact': True, 'isEnabled': False, 'themeType': 'dolor amet enim nulla'}, 'unitCount': 'non occaecat', 'unitId': '85', 'websiteUrl': 'http://kpodzz.sb/wnzcq'}, 'oura': 'qui in', 'owner': 'et non incididunt', 'password': 'id', 'passwordSalt': 'nostrud dolore officia aute', 'passwordType': 'veniam proident', 'patreon': 'in id Duis cupidatat', 'paypal': 'in enim aliquip', 'permanentAvatar': 'http://dummyimage.com/100x100', 'permissions': [{'actions': ['ut nulla enim culpa'], 'adapter': 'dolor sunt', 'approveTime': '1995-12-26 11:24:56', 'approver': 'cillum Lorem in non', 'createdTime': '2016-07-03 10:33:13', 'description': '起最还问求级据参效院易被必快龙。色此眼气求山识取温劳量期单整级林运程。合进走的区来只例力它学书眼术五。再经好流设最非主务些生己没条。很证点四合级信着究放土只原适产道太。次准省除量角变其教达又当反教。', 'displayName': '统象公立', 'domains': ['s.lufkhce@qq.com'], 'effect': 'ad nisi pariatur proident', 'groups': ['fugiat Excepteur'], 'isEnabled': False, 'model': 'nisi aliqua sit', 'name': '则由式设场花看', 'owner': 'ullamco sunt', 'resourceType': 'Duis veniam laboris dolor anim', 'resources': ['voluptate'], 'roles': ['incididunt officia Duis veniam'], 'state': 'laboris minim labore culpa', 'submitter': 'Duis est in', 'users': ['consequat quis nisi']}], 'phone': '13892702437', 'preHash': 'eu', 'preferredMfaType': 'ex quis', 'properties': {'additionalProperties': 'anim ut reprehenderit voluptate ullamco'}, 'qq': 'aute nisi', 'ranking': 86, 'recoveryCodes': ['36'], 'region': 'dolore do reprehenderit ut', 'roles': [{'createdTime': '2014-05-28 06:23:22', 'description': '干好相然取则车期商该应位作产就。斗质都美法斗基建且决结应前各。团向办观质等阶团角者点历力断属。它图社气说代自真次正你型圆头区美高和。速约气她入况头格么品百治已量为。', 'displayName': '报被身权', 'domains': ['l.dvp@qq.com'], 'groups': ['non irure'], 'isEnabled': False, 'name': '共么音构', 'owner': 'aliquip reprehenderit mollit sed', 'roles': ['veniam incididunt cupidatat do'], 'users': ['ullamco est ex aute ad']}], 'salesforce': 'voluptate nostrud occaecat', 'score': 3, 'shopify': 'nisi sit ut', 'signinWrongTimes': 358517472668, 'signupApplication': 'in laborum consectetur', 'slack': 'consequat qui ut eu', 'soundcloud': 'dolor tempor culpa', 'spotify': 'ex minim veniam Ut', 'steam': 'pariatur cupidatat dolore', 'strava': 'qui dolor cupidatat exercitation', 'stripe': 'quis Duis', 'tag': 'elit cillum culpa aute', 'tiktok': 'sint sunt et nisi', 'title': '江始习确市片', 'totpSecret': 'elit do', 'tumblr': 'magna consectetur', 'twitch': 'irure ullamco', 'twitter': 'mollit fugiat exercitation Ut nisi', 'type': 'laborum in eu', 'typetalk': 'laboris in', 'uber': 'anim aute laborum labore', 'updatedTime': '1977-06-28 07:10:41', 'userId': '12', 'vk': 'minim officia', 'web3onboard': 'nostrud', 'webauthnCredentials': [], 'wechat': 'aliqua voluptate', 'wecom': 'consequat cupidatat nisi commodo', 'weibo': 'ea laborum et nostrud', 'wepay': 'dolor minim dolore Duis', 'xero': 'deserunt exercitation Ut anim ad', 'yahoo': 'esse voluptate exercitation', 'yammer': 'in nulla', 'yandex': 'non cupidatat', 'zoom': 'minim tempor qui culpa Lorem'}]}], 'contactEmail': 'j.ctmhybi@qq.com', 'createdTime': '2018-08-28 19:22:27', 'displayName': '动十新今无整', 'educateUnit': 'occaecat incididunt in fugiat labore', 'educateUnitObj': {'administrativeDivisionCity': '张家口市', 'administrativeDivisionCounty': 'labore do sed occaecat enim', 'administrativeDivisionProvince': '内蒙古自治区', 'createdTime': '1971-02-21 09:19:05', 'departmentObjs': [], 'locationAddress': '湖北省阳泉市下陆区', 'locationCity': '陇南市', 'locationCounty': 'consequat', 'locationProvince': '上海', 'owner': 'deserunt sunt sint id', 'unitCode': '60', 'unitId': '3', 'unitName': '除广名很', 'unitType': 'cillum amet occaecat consequat', 'updatedTime': '1972-04-15 08:40:12'}, 'isDeleted': False, 'isEnabled': False, 'isTopGroup': True, 'key': 'eiusmod', 'manager': 'eiusmod do veniam reprehenderit', 'name': '酸部明', 'newCode': '65', 'newType': 'sint consequat deserunt anim', 'owner': 'sint in do adipisicing non', 'parentId': '50', 'parentName': '低感子总天能', 'tags': ['Ut commodo'], 'title': '消程系战起', 'type': 'eu', 'updatedTime': '1985-02-27 10:35:18', 'users': [{'accessKey': 'ipsum cillum Duis non consectetur', 'accessSecret': 'occaecat', 'accountStatus': 'nostrud', 'address': ['云南省宿迁市怀远县'], 'adfs': 'Ut ullamco', 'affiliation': 'velit consequat sit in', 'alipay': 'quis ad', 'amazon': 'in irure qui veniam', 'apple': 'cupidatat et ea pariatur elit', 'auth0': 'pariatur laboris', 'avatar': 'http://dummyimage.com/100x100', 'avatarType': 'http://dummyimage.com/100x100', 'azuread': 'nisi ut fugiat', 'baidu': '67', 'battlenet': 'aliquip occaecat adipisicing', 'bilibili': 'veniam', 'bio': 'Excepteur Ut amet laboris ullamco', 'birthday': '1998-09-16', 'bitbucket': 'cupidatat nostrud ut tempor', 'box': 'aute officia est occaecat aliquip', 'casdoor': 'aute magna', 'cloudfoundry': 'esse aliquip Duis fugiat dolor', 'countryCode': '35', 'createdIp': '236.151.93.195', 'createdTime': '1981-06-01 01:03:38', 'custom': 'consequat minim', 'dailymotion': 'ea non', 'deezer': 'consequat', 'digitalocean': 'dolor ex commodo', 'dingtalk': 'ipsum', 'discord': 'adipisicing quis', 'displayName': '先出听面', 'douyin': 'consequat sit', 'dropbox': 'deserunt irure cupidatat tempor', 'educateUser': {'avatar': 'http://dummyimage.com/100x100', 'birthDate': '1978-08-11', 'createdTime': '2014-03-04 00:52:36', 'currentUnit': 'nostrud cupidatat magna culpa est', 'departmentId': '88', 'departmentNames': '种委己切', 'email': 'b.rmrofqjxki@qq.com', 'gender': '女', 'idCardNumber': '41', 'idCardType': '77', 'identity': '61', 'identityNames': '打线结角下号', 'identityType': '84', 'identityTypeNames': '林学育', 'mainUnitName': '酸那物两月心', 'name': '长水技片完军', 'owner': 'exercitation aute elit Excepteur', 'phoneNumber': '94', 'realName': '思入权', 'sourceApp': 'quis dolore deserunt', 'updatedTime': '2021-08-30 14:57:08', 'userCode': '99', 'userId': '2', 'userStatus': 'magna adipisicing'}, 'education': 'irure in laboris ea in', 'email': 'm.mmrwtk@qq.com', 'emailVerified': False, 'eveonline': 'ad', 'externalId': '25', 'facebook': 'dolore dolor', 'firstName': '空适带化的断', 'fitbit': 'ut et', 'gender': '男', 'gitea': 'nisi aliqua dolor qui elit', 'gitee': 'aute amet irure', 'github': 'laboris esse', 'gitlab': 'deserunt culpa laborum non', 'google': 'velit consequat aute Lorem', 'groups': ['consectetur'], 'hash': 'voluptate eiusmod aliqua velit', 'heroku': 'in dolor', 'homepage': 'quis do sit velit qui', 'id': '87', 'idCard': '52', 'idCardType': '53', 'influxcloud': 'nulla eu est laborum cupidatat', 'infoflow': 'ex eiusmod dolor nisi mollit', 'instagram': 'tempor ipsum', 'intercom': 'reprehenderit commodo', 'isAdmin': False, 'isDefaultAvatar': False, 'isDeleted': False, 'isForbidden': True, 'isOnline': True, 'kakao': 'labore Ut in culpa voluptate', 'karma': 74, 'language': 'fugiat', 'lark': 'dolore', 'lastName': '内思第响共', 'lastSigninIp': '181.184.129.212', 'lastSigninTime': '2009-05-28 04:49:19', 'lastSigninWrongTime': '1983-02-07 03:04:25', 'lastfm': 'Lorem enim sit', 'ldap': 'eiusmod mollit ex occaecat', 'line': 'laborum ut in et', 'linkedin': 'Duis ut', 'location': 'exercitation in ullamco', 'mailru': 'x.jruyepb@qq.com', 'managedAccounts': [{'application': 'reprehenderit dolor elit Ut magna', 'password': 'magna nostrud', 'signinUrl': 'http://supes.gw/eaejtqm', 'username': '林芳'}], 'meetup': 'cupidatat sint tempor', 'metamask': 'culpa elit ex', 'mfaEmailEnabled': True, 'mfaPhoneEnabled': True, 'microsoftonline': 'sed in labore', 'multiFactorAuths': [{'countryCode': '73', 'enabled': False, 'isPreferred': True, 'mfaType': 'tempor culpa nulla dolore', 'recoveryCodes': ['12'], 'secret': 'exercitation', 'url': 'http://jfttvq.no/rqeiosze'}], 'name': '则群着志节合', 'naver': 'ex reprehenderit eu nostrud dolore', 'nextcloud': 'eu nostrud ex', 'okta': 'quis', 'onedrive': 'sunt ullamco minim in', 'orgObj': {'accountItems': [{'modifyRule': 'minim in sint', 'name': '清金知华细听', 'viewRule': 'aute sed', 'visible': True}], 'accountQuantity': '51', 'countryCodes': ['44'], 'createdTime': '2016-10-28 19:47:31', 'defaultApplication': 'laborum', 'defaultAvatar': 'http://dummyimage.com/100x100', 'defaultPassword': 'aliquip magna', 'displayName': '土活争回', 'educateUnits': [{'administrativeDivisionCity': '张家口市', 'administrativeDivisionCounty': 'labore do sed occaecat enim', 'administrativeDivisionProvince': '内蒙古自治区', 'createdTime': '1971-02-21 09:19:05', 'departmentObjs': [], 'locationAddress': '湖北省阳泉市下陆区', 'locationCity': '陇南市', 'locationCounty': 'consequat', 'locationProvince': '上海', 'owner': 'deserunt sunt sint id', 'unitCode': '60', 'unitId': '3', 'unitName': '除广名很', 'unitType': 'cillum amet occaecat consequat', 'updatedTime': '1972-04-15 08:40:12'}], 'enableSoftDeletion': True, 'favicon': 'http://dummyimage.com/100x100', 'initScore': 52, 'isProfilePublic': True, 'languages': ['et aute'], 'masterPassword': 'nisi est in irure Ut', 'mfaItems': [{'name': '格走思技不打构', 'rule': 'proident'}], 'name': '转华斯族风', 'orgType': 'ad pariatur veniam minim eu', 'overview': 'ea enim qui', 'owner': 'Lorem deserunt sed', 'passwordOptions': ['dolor nulla'], 'passwordSalt': 'quis eiusmod reprehenderit tempor', 'passwordType': 'ea nulla', 'status': 'dolor nisi adipisicing', 'tags': ['veniam dolor sunt qui'], 'themeData': {'borderRadius': 13, 'colorPrimary': 'non cillum Excepteur elit consectetur', 'isCompact': False, 'isEnabled': True, 'themeType': 'irure'}, 'unitCount': 'esse aute laboris tempor nulla', 'unitId': '78', 'websiteUrl': 'http://usiehdlm.pl/hbomleqnz'}, 'oura': 'in cupidatat incididunt consequat', 'owner': 'aliqua aute culpa nulla', 'password': 'est amet', 'passwordSalt': 'esse quis laboris Excepteur', 'passwordType': 'in Duis ad', 'patreon': 'in veniam anim commodo laborum', 'paypal': 'consectetur pariatur laboris aute', 'permanentAvatar': 'http://dummyimage.com/100x100', 'permissions': [{'actions': ['enim aliquip ullamco Duis'], 'adapter': 'ut esse', 'approveTime': '2004-09-18 12:05:34', 'approver': 'Lorem sit aute Excepteur voluptate', 'createdTime': '1982-11-19 06:26:43', 'description': '原斗术而果给这区于眼亲带里标正求计。至手公便清热问没指规以般物深素认九。号人十算引自造市里几白一温般为领林。置造往算务连她道反或实收根信观存低龙。今多商元人以影状越论却养通共还正之众。北复眼省北直用风物派成提公少话你积。', 'displayName': '给数酸学', 'domains': ['p.chek@qq.com'], 'effect': 'sunt in non aliqua magna', 'groups': ['ad laborum nostrud Ut incididunt'], 'isEnabled': False, 'model': 'labore incididunt fugiat amet esse', 'name': '开酸却见或他', 'owner': 'officia eiusmod', 'resourceType': 'culpa dolor anim cupidatat', 'resources': ['ipsum laboris'], 'roles': ['laborum culpa esse velit'], 'state': 'in elit quis cupidatat pariatur', 'submitter': 'aliquip ut anim', 'users': ['do']}], 'phone': '18170728388', 'preHash': 'dolore dolor ut', 'preferredMfaType': 'sed', 'properties': {'additionalProperties': 'enim'}, 'qq': 'in elit ut', 'ranking': 70, 'recoveryCodes': ['29'], 'region': 'in aute minim nostrud labore', 'roles': [{'createdTime': '2018-07-02 12:24:41', 'description': '求广方引产将写作市节民体矿三委万选明。华备必油应地儿海广期信眼能王系论研。内从战这在商形是八太情成容最改国自业。书系去书现市头开细已结四角这响。', 'displayName': '也委面求米酸', 'domains': ['p.knfquvoc@qq.com'], 'groups': ['Duis sit amet'], 'isEnabled': False, 'name': '或片严', 'owner': 'esse id sit amet ut', 'roles': ['dolor adipisicing tempor reprehenderit ea'], 'users': ['velit ea eu deserunt sunt']}], 'salesforce': 'occaecat pariatur amet', 'score': 94, 'shopify': 'sint nisi dolor Lorem', 'signinWrongTimes': 1438792728370, 'signupApplication': 'anim', 'slack': 'amet cupidatat consequat', 'soundcloud': 'do', 'spotify': 'labore tempor quis dolor', 'steam': 'consectetur adipisicing', 'strava': 'tempor', 'stripe': 'in Ut', 'tag': 'do in consectetur sed', 'tiktok': 'voluptate anim in Duis nostrud', 'title': '却行图好被权', 'totpSecret': 'sunt ipsum sit in', 'tumblr': 'amet ad sit et consequat', 'twitch': 'Ut Excepteur', 'twitter': 'ipsum', 'type': 'laboris ullamco sint', 'typetalk': 'ipsum', 'uber': 'cupidatat sint', 'updatedTime': '1971-02-02 11:23:26', 'userId': '16', 'vk': 'deserunt amet', 'web3onboard': 'dolore ipsum fugiat eu magna', 'webauthnCredentials': [], 'wechat': 'irure aliquip', 'wecom': 'sit', 'weibo': 'ex qui', 'wepay': 'officia', 'xero': 'ullamco id adipisicing', 'yahoo': 'fugiat nostrud sed et', 'yammer': 'sunt pariatur', 'yandex': 'cillum do pariatur', 'zoom': 'Excepteur fugiat incididunt cillum et'}]}], 'locationAddress': '湖北省阳泉市下陆区', 'locationCity': '陇南市', 'locationCounty': 'consequat', 'locationProvince': '上海', 'owner': 'deserunt sunt sint id', 'unitCode': '60', 'unitId': '3', 'unitName': '除广名很', 'unitType': 'cillum amet occaecat consequat', 'updatedTime': '1972-04-15 08:40:12'}



        apiname = '/api/add-educate-unit'
        # 字典参数
        datadict = dict_data
        if isinstance(datadict['createdTime'], (date, datetime)):
            datadict['createdTime'] = datadict['createdTime'].strftime("%Y-%m-%d %H:%M:%S")

        # if isinstance(datadict['createdTime'], (date, datetime)):
        #     datadict['createdTime'] = datadict['createdTime'].strftime("%Y-%m-%d %H:%M:%S")
        datadict=convert_dates_to_strings(datadict)
        print(datadict,'字典参数')


        response = await send_orgcenter_request(apiname,datadict,'post',False)
        print(response,'接口响应')
        try:
            print(response)



            return response
        except Exception as e:
            print(e)
            raise e
            return response

        return None