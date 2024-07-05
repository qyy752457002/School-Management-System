import hashlib
import json
from datetime import datetime

import shortuuid
from mini_framework.utils.http import HTTPRequest
from mini_framework.utils.json import JsonUtils
from mini_framework.utils.snowflake import SnowflakeIdGenerator

from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from pydantic import BaseModel

from daos.institution_dao import InstitutionDAO
from models.institution import Institution
from models.student_transaction import AuditAction
from rules.common.common_rule import send_request
from rules.school_rule import SchoolRule
from rules.system_rule import SystemRule
from views.common.common_view import workflow_service_config
from views.models.institutions import Institutions as InstitutionModel, Institutions, InstitutionKeyInfo, \
    InstitutionOptional
from views.models.planning_school import PlanningSchoolTransactionAudit, PlanningSchoolStatus
from views.models.system import SCHOOL_OPEN_WORKFLOW_CODE, INSTITUTION_OPEN_WORKFLOW_CODE, SCHOOL_CLOSE_WORKFLOW_CODE, \
    INSTITUTION_CLOSE_WORKFLOW_CODE, SCHOOL_KEYINFO_CHANGE_WORKFLOW_CODE, INSTITUTION_KEYINFO_CHANGE_WORKFLOW_CODE


@dataclass_inject
class InstitutionRule(SchoolRule):

    async def add_school_keyinfo_change_work_flow(self, school_flow: InstitutionKeyInfo,process_code=None):
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
        mapa['school_id'] = school_flow.id
        datadict['json_data'] =  json.dumps(mapa, ensure_ascii=False)
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


    pass