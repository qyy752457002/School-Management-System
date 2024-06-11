from datetime import datetime
from typing import List

from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task import Task
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.views import BaseView
from starlette.requests import Request

from rules.operation_record import OperationRecordRule
from views.common.common_view import compare_modify_fields, get_extend_params
from views.models.extend_params import ExtendParams
from views.models.operation_record import OperationRecord, OperationModule, OperationTargetType, OperationType
from views.models.planning_school import PlanningSchoolStatus, PlanningSchoolFounderType
from views.models.school_communications import SchoolCommunications
from views.models.school_eduinfo import SchoolEduInfo
from views.models.school import School, SchoolBaseInfo, SchoolKeyInfo, SchoolKeyAddInfo, SchoolBaseInfoOptional, \
    SchoolTask

from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse

from rules.school_eduinfo_rule import SchoolEduinfoRule
from rules.school_rule import SchoolRule

from rules.school_communication_rule import SchoolCommunicationRule


class SchoolView(BaseView):
    def __init__(self):
        super().__init__()
        self.school_rule = get_injector(SchoolRule)
        self.school_eduinfo_rule = get_injector(SchoolEduinfoRule)
        self.school_communication_rule = get_injector(SchoolCommunicationRule)
        self.operation_record_rule = get_injector(OperationRecordRule)

    async def get(self,
                  school_no: str = Query(None, title="学校编号", description="学校编号", min_length=1, max_length=20,
                                         example=''),
                  school_name: str = Query(None, description="学校名称", min_length=1, max_length=20, example=''),
                  school_id: int = Query(..., description="学校id|根据学校查规划校", example='1'),
                  ):
        school = await self.school_rule.get_school_by_id(school_id)
        school_keyinfo = await self.school_rule.get_school_by_id(school_id, extra_model=SchoolKeyInfo)

        school_eduinfo={}
        school_communication = await self.school_communication_rule.get_school_communication_by_school_id(school_id)
        # todo 异常可能导致orm转换时 的链接释放
        try:

            school_eduinfo = await self.school_eduinfo_rule.get_school_eduinfo_by_school_id(school_id)
        except Exception as e:
            print(e)


        return {'school': school, 'school_communication': school_communication, 'school_eduinfo': school_eduinfo,
                'school_keyinfo': school_keyinfo}

    async def post(self, school: SchoolKeyAddInfo):
        res = await self.school_rule.add_school(school)
        print(res)
        resc = SchoolCommunications(id=0)
        # logging.debug(resc,'模型2', res.id, type( res.id ))
        newid = str(res.id)
        print(resc, '模型23', res.id, type(res.id))
        # str( res.id).copy()

        resc.school_id = int(newid)
        print(resc, newid, '||||||||')

        # 保存通信信息
        res_comm = await self.school_communication_rule.add_school_communication(resc,
                                                                                 convertmodel=False)
        print(res_comm, '模型2 res')
        #
        resedu = SchoolEduInfo(id=0)
        resedu.school_id = res.id
        # 保存教育信息
        res_edu = await self.school_eduinfo_rule.add_school_eduinfo(resedu, convertmodel=False)
        print(res_edu)

        return res
        # return  school

    # # 修改 关键信息
    async def put_keyinfo(self,
                          school: SchoolKeyInfo,
                          # planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),

                          ):
        origin = await self.school_rule.get_school_by_id(school.id)

        res2 = compare_modify_fields(school, origin)
        # print(  res2)

        res = await self.school_rule.update_school(school)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(school.id),
            operator='admin',
            module=OperationModule.KEYINFO.value,
            target=OperationTargetType.SCHOOL.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data=str(res2)[0:1000],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='', ))

        return res
        # return  {school_no,borough,block }

    # 删除
    async def delete(self, school_id: str = Query(..., title="学校编号", description="学校id/园所id", min_length=1,
                                                  max_length=20, example='SC2032633'), ):
        print(school_id)
        res = await self.school_rule.softdelete_school(school_id)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(school_id),
            operator='admin',
            module=OperationModule.KEYINFO.value,
            target=OperationTargetType.SCHOOL.value,

            action_type=OperationType.DELETE.value,
            ip='127.0.0.1',
            change_data=str(res)[0:1000],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='', ))

        return res
        # return  school_id

    # 修改 变更 基本信息
    async def patch_baseinfo(self, school_baseinfo: SchoolBaseInfo):
        origin = await self.school_rule.get_school_by_id(school_baseinfo.id)
        log_con = compare_modify_fields(school_baseinfo, origin)

        res = await self.school_rule.update_school_byargs(school_baseinfo, 2)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(school_baseinfo.id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.SCHOOL.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data=str(log_con)[0:1000],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='', ))

        return res

    async def page(self,
                   page_request=Depends(PageRequest),
                   block: str = Query("", title=" ", description="地域管辖区", ),
                   school_code: str = Query("", title="", description=" 园所标识码", ),
                   school_level: str = Query("", title="", description=" 学校星级", ),
                   borough: str = Query("", title="  ", description=" 行政管辖区", ),
                   status: PlanningSchoolStatus = Query("", title="", description=" 状态", examples=['正常']),

                   founder_type: List[PlanningSchoolFounderType] = Query([], title="", description="举办者类型",
                                                                         examples=['地方']),
                   founder_type_lv2: List[str] = Query([], title="", description="举办者类型二级",
                                                       examples=['教育部门']),
                   founder_type_lv3: List[str] = Query([], title="", description="举办者类型三级",
                                                       examples=['县级教育部门']),

                   school_no: str = Query(None, title="学校编号", description="学校编号", min_length=1, max_length=20,
                                          example='SC2032633'),
                   school_name: str = Query(None, description="学校名称", min_length=1, max_length=20,
                                            example='XX小学'),
                   planning_school_id: int = Query(None, description="规划校ID", example='1'),
                   province: str = Query("", title="", description="省份代码", ),
                   city: str = Query("", title="", description="城市", ),

                   ):
        print(page_request)
        items = []

        paging_result = await self.school_rule.query_school_with_page(page_request,
                                                                      school_name, school_no, school_code,
                                                                      block, school_level, borough, status,
                                                                      founder_type,
                                                                      founder_type_lv2,
                                                                      founder_type_lv3, planning_school_id, province,
                                                                      city)
        return paging_result

    # 开办
    async def patch_open(self, school_id: str = Query(..., title="学校编号", description="学校id/园所id", min_length=1,
                                                      max_length=20, example='SC2032633')):
        # print(school)
        res = await self.school_rule.update_school_status(school_id, PlanningSchoolStatus.NORMAL.value, 'open')
        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(school_id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.SCHOOL.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data=str(school_id)[0:1000],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='', ))

        return res

    # 关闭
    async def patch_close(self, school_id: str = Query(..., title="学校编号", description="学校id/园所id", min_length=1,
                                                       max_length=20, example='SC2032633'),
                          action_reason: str = Query(None, description="原因", min_length=1, max_length=20,
                                                     example='家庭搬迁'),
                          related_license_upload: List[str] = Query(None, description="相关证照上传", min_length=1,
                                                                    max_length=60, example=''),
                          ):
        res = await self.school_rule.update_school_status(school_id, PlanningSchoolStatus.CLOSED.value)
        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(school_id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.SCHOOL.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data=str(school_id)[0:1000],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='', ))

        return res



    # 更新 全部信息 用于页面的 暂存 操作  不校验 数据的合法性
    async def put(self,

                  school: SchoolBaseInfoOptional,
                  school_communication: SchoolCommunications,
                  school_eduinfo: SchoolEduInfo,
                  school_id: int = Query(..., title="", description="学校id/园所id", example='38'),

                  ):
        # print(planning_school)
        school.id = school_id
        school_communication.school_id = school_id
        school_eduinfo.school_id = school_id
        school_communication.id = None
        school_eduinfo.id = None
        # if isinstance(school_eduinfo.att_class_type,  bool):
        #     school_eduinfo.att_class_type= str( school_eduinfo.att_class_type )

        origin = await self.school_rule.get_school_by_id(school.id)
        log_con = compare_modify_fields(school, origin)

        res = await self.school_rule.update_school_byargs(school)
        res_com = await self.school_communication_rule.update_school_communication_byargs(
            school_communication)
        res_edu = await self.school_eduinfo_rule.update_school_eduinfo_byargs(school_eduinfo)

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(school_id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.SCHOOL.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data=str(log_con)[0:1000],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='', ))

        return res

    # 正式开办  传全部  插入或者更新
    async def put_open(self,

                       school: SchoolBaseInfo,
                       school_communication: SchoolCommunications,
                       school_eduinfo: SchoolEduInfo,
                       school_id: int = Query(..., title="", description="学校id/园所id", example='38'),

                       ):
        # print(planning_school)
        school.id = school_id
        school_communication.school_id = school_id
        school_eduinfo.school_id = school_id
        school_communication.id = None
        school_communication.id = None
        # if isinstance(school_eduinfo.att_class_type,  bool):
        #     school_eduinfo.att_class_type= str( school_eduinfo.att_class_type )
        delattr(school, 'status')

        origin = await self.school_rule.get_school_by_id(school.id)
        log_con = compare_modify_fields(school, origin)

        res = await self.school_rule.update_school_byargs(school)
        res_com = await self.school_communication_rule.update_school_communication_byargs(
            school_communication)
        res_edu = await self.school_eduinfo_rule.update_school_eduinfo_byargs(school_eduinfo)

        #  调用 内部方法 开办

        res2 = await self.patch_open(str(school_id))

        #  记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(school_id),
            operator='admin',
            module=OperationModule.BASEINFO.value,
            target=OperationTargetType.PLANNING_SCHOOL.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data=str(log_con)[0:1000],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
            account='', ))

        return res2
    # 学校搜索 模糊搜索
    async def get_search(self,
                         request: Request  ,

                         school_name: str = Query("", title="学校名称", description="1-20字符", ),

                         page_request=Depends(PageRequest),

    ):
        items = []
        # 学校 区 只能看自己的范围内的数据
        paging_result = await self.school_rule.query_schools(school_name,await get_extend_params(request))
        return paging_result
    # 学校开设审核
    async def patch_open_audit(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                     min_length=1, max_length=20, example='SC2032633')):
        pass
    # 学校关闭审核
    async def patch_close_audit(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                      min_length=1, max_length=20, example='SC2032633')):
        pass
    # 学校关键信息变更审核
    async def patch_keyinfo_audit(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                        min_length=1, max_length=20, example='SC2032633')):
        pass


    # 导入   任务队列的
    async def post_school_import(self,
                                 filename: str = Query(..., description="文件名"),
                                 bucket: str = Query(..., description="文件名"),
                                 scene: str = Query('', description="文件名"),
                                 ) -> Task:
        task = Task(
            #todo sourcefile无法记录3个参数  故 暂时用3个参数来实现  需要 在cofnig里有配置   对应task类里也要有这个 键
            task_type="school_import",
            # 文件 要对应的 视图模型
            payload=SchoolTask(file_name=filename, bucket=bucket, scene=scene),
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task