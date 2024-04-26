from datetime import datetime
from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.operation_record import OperationRecordRule
from views.common.common_view import compare_modify_fields
from views.models.campus import Campus, CampusBaseInfo, CampusKeyInfo, CampusKeyAddInfo
# from fastapi import Field

from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from rules.campus_rule import CampusRule
from views.models.campus_communications import CampusCommunications
from rules.campus_communication_rule import CampusCommunicationRule
from views.models.campus_eduinfo import CampusEduInfo
from rules.campus_eduinfo_rule import CampusEduinfoRule
from views.models.operation_record import OperationRecord, OperationModule, OperationTargetType, OperationType
from views.models.planning_school import PlanningSchoolStatus, PlanningSchoolFounderType


class CampusView(BaseView):
    def __init__(self):
        super().__init__()
        self.campus_rule = get_injector( CampusRule)
        self.campus_communication_rule = get_injector( CampusCommunicationRule)
        self.campus_eduinfo_rule = get_injector( CampusEduinfoRule)
        self.operation_record_rule =   get_injector(OperationRecordRule)




    async def get(self,
                  campus_id: int = Query(..., description="校区id", example='1'),

                  ):
        campus =await self.campus_rule.get_campus_by_id(campus_id)
        campus_communication = await self.campus_communication_rule.get_campus_communication_by_campus_id(campus_id)
        campus_eduinfo = await self.campus_eduinfo_rule.get_campus_eduinfo_by_campus_id(campus_id)
        campus_keyinfo = await self.campus_rule.get_campus_by_id(campus_id,extra_model=CampusKeyInfo)

        return {'campus':campus,'campus_communication':campus_communication ,'campus_eduinfo':campus_eduinfo,'campus_keyinfo':campus_keyinfo }

        # return  res

    async def post(self,campus:CampusKeyAddInfo):
        print(campus)
        res =await  self.campus_rule.add_campus(campus)

        #
        # resc = CampusCommunications(id=0)
        # # logging.debug(resc,'模型2', res.id, type( res.id ))
        # newid = str(res.id)
        # print(resc, '模型23', res.id, type(res.id))
        # # str( res.id).copy()
        #
        # resc.campus_id = int(newid)
        # print(resc, newid, '||||||||')
        #
        # # 保存通信信息
        # res_comm = await self.campus_communication_rule.add_campus_communication(resc,
        #                                                                          convertmodel=False)
        # print(res_comm, '模型2 res')
        # #
        # resedu = CampusEduInfo(id=0)
        # resedu.campus_id = res.id
        # # 保存教育信息
        # res_edu = await self.campus_eduinfo_rule.add_campus_eduinfo(resedu, convertmodel=False)
        # print(res_edu)

        return  res

    # 修改 关键信息
    async def put_keyinfo(self,
                  campus_keyinfo:CampusKeyInfo
                  ):
        # print(campus)

        origin = await self.campus_rule.get_campus_by_id(campus_keyinfo.id)

        res2 =  compare_modify_fields(campus_keyinfo,origin)

        res = await self.campus_rule.update_campus(campus_keyinfo)
        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(campus_keyinfo.id),
            operator='admin',
            module=OperationModule.KEYINFO.value,
            target=OperationTargetType.CAMPUS.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data= str(res2)[ 0:1000 ],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='',))

        return  res
    # 删除
    async def delete(self, campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='1'),):
        print(campus_id)
        res = await self.campus_rule.softdelete_campus(campus_id)
        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(campus_id),
            operator='admin',
            module=OperationModule.KEYINFO.value,
            target=OperationTargetType.CAMPUS.value,

            action_type=OperationType.DELETE.value,
            ip='127.0.0.1',
            change_data= str(res)[ 0:1000 ],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='',))

        return  res
    # 修改 变更 基本信息
    async def patch_baseinfo(self, campus_baseinfo:CampusBaseInfo
                               ):
        # print(campus)

        origin = await self.campus_rule.get_campus_by_id(campus_baseinfo.id)
        log_con =  compare_modify_fields(campus_baseinfo,origin)
        res = await self.campus_rule.update_campus(campus_baseinfo,2)
        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(campus_baseinfo.id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.CAMPUS.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data= str(log_con)[ 0:1000 ],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='',))
        return   res




    async def page(self,
                   page_request= Depends(PageRequest),
                   campus_no:str= Query(None, title="校区编号", description="校区编号",min_length=1,max_length=20,example='SC2032633'),
                   campus_name:str= Query(None, description="校区名称" ,min_length=1,max_length=20,example='XX小学'),
                   block: str = Query("", title=" ", description="地域管辖区", ),
                   campus_code: str = Query("", title="", description=" 校区标识码", ),
                   campus_level: str = Query("", title="", description=" 学校星级", ),
                   borough:str=Query("", title="  ", description=" 行政管辖区", ),
                   status: PlanningSchoolStatus = Query("", title="", description=" 状态",examples=['正常']),

                   founder_type: List[ PlanningSchoolFounderType]  = Query([], title="", description="举办者类型",examples=['地方']),
                   founder_type_lv2:  List[ str] = Query([], title="", description="举办者类型二级",examples=['教育部门']),
                   founder_type_lv3:  List[ str] = Query([], title="", description="举办者类型三级",examples=['县级教育部门']),

                   school_id:int= Query(None, description="学校ID" , example='1'),

                   ):
        print(page_request)
        items=[]

        paging_result = await self.campus_rule.query_campus_with_page(page_request,
                                                                      campus_name,campus_no,campus_code,
                                                                      block,campus_level,borough,status,founder_type,
                                                                      founder_type_lv2,
                                                                      founder_type_lv3,school_id )
        return paging_result




    # 开办
    async def patch_open(self,campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='1')):
        # print(campus)
        res = await self.campus_rule.update_campus_status(campus_id , PlanningSchoolStatus.NORMAL.value)
        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(campus_id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.CAMPUS.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data= str(campus_id)[ 0:1000 ],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='',))

        return  res

    # 关闭
    async def patch_close(self,campus_id:str= Query(..., title="校区编号", description="校区id/园所id",min_length=1,max_length=20,example='1')):
        # print(campus)
        res = await self.campus_rule.update_campus_status(campus_id , PlanningSchoolStatus.CLOSED.value)
        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(campus_id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.CAMPUS.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data= str(campus_id)[ 0:1000 ],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='',))

        return  res

    # 导入 todo 任务队列的
    async def importing(self,campus:Campus):
        print(campus)
        return  campus
    #
    # async def get_extinfo(self):
    #     #
    #     return [ ]
    # 新增 通信信息
    # async def post_comminfo(self,
    #                         campus: CampusCommunications,
    #
    #                         ):
    #
    #     res = await self.campus_communication_rule.add_campus_communication(campus)
    #
    #     # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
    #
    #     return res
    #
    # # 新增 教学信息
    # async def post_eduinfo(self,
    #                        campus: CampusEduInfo,
    #
    #                        ):
    #
    #     res = await self.campus_eduinfo_rule.add_campus_eduinfo(campus)
    #
    #     # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
    #
    #     return res

    # 更新 全部信息 用于页面的 暂存 操作  不校验 数据的合法性
    async def put(self,
                  campus:CampusKeyAddInfo,

                  # campus: CampusBaseInfo,
                  # campus_communication: CampusCommunications,
                  # campus_eduinfo: CampusEduInfo,
                  campus_id: int = Query(..., title="", description="校区id", example='38'),

                  ):
        # print(planning_campus)
        campus.id = campus_id
        # campus_communication.campus_id = campus_id
        # campus_eduinfo.campus_id = campus_id
        origin = await self.campus_rule.get_campus_by_id(campus.id)
        log_con =  compare_modify_fields(campus,origin)

        res = await self.campus_rule.update_campus_byargs(campus)
        # res_com = await self.campus_communication_rule.update_campus_communication_byargs(
        #     campus_communication)
        # res_edu = await self.campus_eduinfo_rule.update_campus_eduinfo_byargs(campus_eduinfo)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(campus_id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.CAMPUS.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data= str(log_con)[ 0:1000 ],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='',))

        return res


    async def get_search(self,
                         campus_name: str = Query("", title="校区名称", description="1-20字符",),

                         page_request=Depends(PageRequest) ):
        print(page_request,)
        items = []
        # exit(1)
        # return page_search
        paging_result = await self.campus_rule.query_campus(campus_name)
        return paging_result
