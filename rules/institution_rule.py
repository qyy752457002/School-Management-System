import copy
import hashlib
import json
import os
from datetime import datetime, date

import shortuuid
from mini_framework.async_task.data_access.models import TaskResult
from mini_framework.async_task.task.task import Task, TaskState
from mini_framework.data.tasks.excel_tasks import ExcelWriter
from mini_framework.storage.manager import storage_manager
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.logging import logger
from mini_framework.utils.snowflake import SnowflakeIdGenerator

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from pydantic import BaseModel

from daos.institution_dao import InstitutionDAO
from models.institution import Institution
from models.student_transaction import AuditAction
from rules.common.common_rule import send_request, send_orgcenter_request
from rules.school_rule import SchoolRule
from rules.system_rule import SystemRule
from views.common.common_view import workflow_service_config, map_keys, convert_dates_to_strings
from views.models.institutions import Institutions as InstitutionModel, Institutions, InstitutionKeyInfo, \
    InstitutionOptional, InstitutionBaseInfo, InstitutionPageSearch
from views.models.planning_school import PlanningSchoolTransactionAudit, PlanningSchoolStatus
from views.models.system import SCHOOL_OPEN_WORKFLOW_CODE, INSTITUTION_OPEN_WORKFLOW_CODE, SCHOOL_CLOSE_WORKFLOW_CODE, \
    INSTITUTION_CLOSE_WORKFLOW_CODE, SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE, \
    InstitutionType
from views.models.school import School as SchoolModel, SchoolKeyAddInfo, SchoolKeyInfo, SchoolBaseInfoOptional
from views.models.planning_school import PlanningSchool as PlanningSchoolModel, PlanningSchoolStatus


@dataclass_inject
class InstitutionRule(SchoolRule):

    async def add_school_keyinfo_change_work_flow(self, school_flow: InstitutionKeyInfo,process_code=None,institution_info=None):
        # school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE
        if process_code:
            datadict['process_code'] = process_code
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        datadict['school_no'] = school_flow.school_no

        datadict['school_name'] = school_flow.school_name
        # datadict['school_edu_level'] =   school_flow.school_edu_level
        datadict['block'] =   school_flow.block
        datadict['borough'] =   school_flow.borough
        # datadict['school_level'] =   school_flow.school_level
        # datadict['school_category'] =   school_flow.school_category
        # datadict['school_operation_type'] =   school_flow.school_operation_type
        # datadict['school_org_type'] =   school_flow.school_org_type

        datadict['apply_user'] =  'tester'
        mapa = school_flow.__dict__
        mapb = institution_info.__dict__
        mapa['institution_id'] = school_flow.id
        # 合并info
        mapb.update(mapa)
        mapb = map_keys(mapb, self.other_mapper)
        datadict['json_data'] =  json.dumps(mapb, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        # url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict,headerdict)
        response= None
        try:
            response = await httpreq.post_json(url,datadict,headerdict)
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response


    # 向工作流中心发送申请
    async def add_school_work_flow(self, school_flow: InstitutionBaseInfo,):
        # school_flow.id=0
        httpreq= HTTPRequest()
        url= workflow_service_config.workflow_config.get("url")
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = INSTITUTION_OPEN_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        # datadict['school_code'] = school_flow.school_code
        datadict['school_name'] = school_flow.school_name
        # datadict['founder_type_lv3'] =   school_flow.founder_type_lv3
        # datadict['block'] =   school_flow.block
        # datadict['borough'] =   school_flow.borough
        # datadict['school_level'] =   school_flow.school_level
        datadict['school_no'] =   school_flow.school_no
        datadict['apply_user'] =  'tester'
        dicta = school_flow.__dict__
        dicta['institution_id'] = school_flow.id
        dicta = map_keys(dicta, self.other_mapper)

        datadict['json_data'] =  json.dumps(dicta, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'
        url=url+apiname
        headerdict = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        # 如果是query 需要拼接参数
        # url+=  ('?' +urlencode(datadict))
        print('参数', url, datadict,headerdict)
        response= None
        try:
            response = await httpreq.post_json(url,datadict,headerdict)
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response


    async def add_school_close_work_flow(self, school_flow: InstitutionBaseInfo,action_reason,related_license_upload):
        # school_flow.id=0
        data= school_flow
        datadict =  data.__dict__
        datadict['process_code'] = INSTITUTION_CLOSE_WORKFLOW_CODE
        datadict['teacher_id'] =  0
        datadict['applicant_name'] =  'tester'
        # datadict['school_code'] = school_flow.school_code
        datadict['school_name'] = school_flow.school_name
        # datadict['founder_type_lv3'] =   school_flow.founder_type_lv3
        # datadict['block'] =   school_flow.block
        # datadict['borough'] =   school_flow.borough
        # datadict['school_level'] =   school_flow.school_level
        datadict['school_no'] =   school_flow.school_no

        datadict['apply_user'] =  'tester'
        dicta = school_flow.__dict__
        dicta['action_reason']= action_reason
        dicta['related_license_upload']= related_license_upload
        dicta['institution_id'] = school_flow.id
        dicta = map_keys(dicta, self.other_mapper)

        datadict['json_data'] =  json.dumps(dicta, ensure_ascii=False)
        apiname = '/api/school/v1/teacher-workflow/work-flow-instance-initiate-test'

        response= None
        try:
            response = await send_request(apiname,datadict,'post')
            print('请求工作流结果',response)
        except Exception as e:
            print(e)
        return response

    async def deal_school(self,process_instance_id ,action, ):
        #  读取流程实例ID
        school = await self.school_dao.get_school_by_process_instance_id(process_instance_id)
        if not school:
            print('未查到事业单位信息',process_instance_id)
            return
        if action=='open':
            res = await self.update_school_status(school.id,  PlanningSchoolStatus.NORMAL.value, 'open')
            await self.send_school_to_org_center(school)
            await self.send_admin_to_org_center(school)
        if action=='close':
            res = await self.update_school_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
        if action=='keyinfo_change':
            # todo 把基本信息变更 改进去
            # res = await self.update_school_status(school.id,  PlanningSchoolStatus.CLOSED.value, 'close')
            # 读取流程的原始信息  更新到数据库
            result = await self.system_rule.get_work_flow_instance_by_process_instance_id(
                process_instance_id)
            if not result.get('json_data'):
                # return {'工作流数据异常 无法解析'}
                pass
            json_data =  JsonUtils.json_str_to_dict(  result.get('json_data'))
            print(json_data)
            # 拿到的是 实际模型的数下  和 需要校验的原始的 键不同   这里转为 原始的键 先
            json_data= map_keys(json_data, self.other_mapper)
            # obj = view_model_to_orm_model(json_data, InstitutionKeyInfo,other_mapper=self.other_mapper)

            planning_school_orm = InstitutionKeyInfo( **json_data)
            planning_school_orm.id= school.id

            res = await self.update_school_byargs(  planning_school_orm)
            pass

        # res = await self.update_school_status(school_id,  PlanningSchoolStatus.NORMAL.value, 'open')

        pass


    async def institution_export(self, task: Task):
        bucket = 'school'
        print(bucket,'桶')

        export_params: InstitutionPageSearch = (
            task.payload if task.payload is InstitutionPageSearch() else InstitutionPageSearch()
        )
        page_request = PageRequest(page=1, per_page=100)
        random_file_name = f"institution_export{shortuuid.uuid()}.xlsx"
        # 获取当前脚本所在目录的绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取当前脚本所在目录的父目录
        parent_dir = os.path.dirname(script_dir)

        # 构建与 script_dir 并列的 temp 目录的路径
        temp_dir_path = os.path.join(parent_dir, 'temp')

        # 确保 temp 目录存在，如果不存在则创建它
        os.makedirs(temp_dir_path, exist_ok=True)
        temp_file_path = os.path.join(temp_dir_path, random_file_name)
        while True:
            # todo  这里的参数需要 解包
            paging = await self.school_dao.query_school_with_page(
                page_request, export_params.school_name,export_params.school_no,export_params.school_code,
                export_params.block,export_params.school_level,export_params.borough,export_params.status,export_params.founder_type,
                export_params.founder_type_lv2,
                export_params.founder_type_lv3 ,export_params.planning_school_id,export_params.province,export_params.city,export_params.institution_category,
            )
            paging_result = PaginatedResponse.from_paging(
                paging, SchoolBaseInfoOptional, {"hash_password": "password"}
            )
            # 处理每个里面的状态 1. 0
            await self.convert_school_to_export_format(paging_result)
            logger.info('分页的结果条数',len(paging_result.items))
            excel_writer = ExcelWriter()
            excel_writer.add_data("Sheet1", paging_result.items)
            excel_writer.set_data(temp_file_path)
            excel_writer.execute()
            # break
            if len(paging.items) < page_request.per_page:
                break
            page_request.page += 1
        #     保存文件时可能报错
        print('临时文件路径',temp_file_path)
        file_storage =  storage_manager.put_file_to_object(
            bucket, f"{random_file_name}.xlsx", temp_file_path
        )
        # 这里会写入 task result 提示 缺乏 result file id  导致报错
        try:

            file_storage_resp = await storage_manager.add_file(
                self.file_storage_dao, file_storage
            )
            print('file_storage_resp ',file_storage_resp)

            task_result = TaskResult()
            task_result.task_id = task.task_id
            task_result.result_file = file_storage_resp.file_name
            task_result.result_bucket = file_storage_resp.virtual_bucket_name
            task_result.result_file_id = file_storage_resp.file_id
            task_result.last_updated = datetime.now()
            task_result.result_id = shortuuid.uuid()
            task_result.state = TaskState.succeeded
            task_result.result_extra = {"file_size": file_storage.file_size}
            if not task_result.result_file_id:
                task_result.result_file_id =  0
            print('拼接数据task_result ',task_result)

            resadd = await self.task_dao.add_task_result(task_result,True)
            print('task_result写入结果',resadd)
        except Exception as e:
            logger.debug('保存文件记录和插入taskresult 失败')

            logger.error(e)
            task_result = TaskResult()

        return task_result
    async def send_school_to_org_center(self,exists_planning_school_origin):
        exists_planning_school= copy.deepcopy(exists_planning_school_origin)
        if isinstance(exists_planning_school.updated_at, (date, datetime)):
            exists_planning_school.updated_at =exists_planning_school.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # 教育单位的类型-必填 administrative_unit|public_institutions|school|developer
        if exists_planning_school_origin.institution_category == InstitutionType.ADMINISTRATION:
            exists_planning_school.institution_category = 'administrative_unit'
        elif exists_planning_school_origin.institution_category == InstitutionType.INSTITUTION:
            exists_planning_school.institution_category = 'public_institutions'
        else:
            exists_planning_school.institution_category = 'school'

        planning_school_communication = await self.school_communication_dao.get_school_communication_by_school_id(exists_planning_school.id)
        cn_exists_planning_school = await self.convert_school_to_export_format(exists_planning_school )
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