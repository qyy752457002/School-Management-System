import logging
from datetime import datetime
from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from business_exceptions.planning_school import PlanningSchoolValidateError, PlanningSchoolBaseInfoValidateError
from rules.operation_record import OperationRecordRule
from views.models.operation_record import OperationRecord, OperationModule, OperationTargetType, OperationType
from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo, PlanningSchoolKeyInfo, \
    PlanningSchoolStatus, PlanningSchoolFounderType, PlanningSchoolPageSearch, PlanningSchoolKeyAddInfo, \
    PlanningSchoolBaseInfoOptional
from views.models.planning_school_communications import PlanningSchoolCommunications
from views.models.planning_school_eduinfo import PlanningSchoolEduInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends, Body
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse

from models.grade import Grade
from rules.planning_school_rule import PlanningSchoolRule
from views.models.grades import Grades
from rules.planning_school_communication_rule import PlanningSchoolCommunicationRule

from rules.planning_school_eduinfo_rule import PlanningSchoolEduinfoRule


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class CustomValidationError:
    pass


class PlanningSchoolView(BaseView):
    def __init__(self):
        super().__init__()
        self.planning_school_rule = get_injector(PlanningSchoolRule)
        self.planning_school_communication_rule = get_injector(PlanningSchoolCommunicationRule)
        self.planning_school_eduinfo_rule = get_injector(PlanningSchoolEduinfoRule)
        self.operation_record_rule =   get_injector(OperationRecordRule)

    # todo  包含3部分信息 1.基本信息 2.通讯信息 3.教育信息
    async def get(self, planning_school_no: str = Query(None, title="学校编号", description="学校编号", min_length=1,
                                                        max_length=20, example='SC2032633'),
                  planning_school_name: str = Query(None, description="学校名称", min_length=1, max_length=20,
                                                    example='XX小学'),
                  planning_school_id: int = Query(..., description="学校id|根据学校查规划校", example='1'),

                  ):
        planning_school , extra_model= await self.planning_school_rule.get_planning_school_by_id(planning_school_id,PlanningSchoolKeyInfo)
        planning_school_communication = await self.planning_school_communication_rule.get_planning_school_communication_by_planning_shcool_id(
            planning_school_id)
        planning_school_eduinfo = await self.planning_school_eduinfo_rule.get_planning_school_eduinfo_by_planning_school_id(
            planning_school_id)

        return {'planning_school': planning_school, 'planning_school_communication': planning_school_communication,
                'planning_school_eduinfo': planning_school_eduinfo,'planning_school_keyinfo':extra_model }

    # 获取单个详情
    # async def get_detail(self, planning_school_no: str = Query(None, title="学校编号", description="学校编号", min_length=1,
    #                                                     max_length=20, example='SC2032633'),
    #               planning_school_name: str = Query(None, description="学校名称", min_length=1, max_length=20,
    #                                                 example='XX小学'),
    #               planning_school_id: int = Query(..., description="学校id|根据学校查规划校", example='1'),
    #
    #               ):
    #     planning_school = await self.planning_school_rule.get_planning_school_by_id(planning_school_id)
    #     return planning_school

    #  新增的实际结果  ID赋值
    # async def post(self, planning_school: PlanningSchool):
    #     print(planning_school)
    #     res = await self.planning_school_rule.add_planning_school(planning_school)
    #
    #     return res
    async def post(self, planning_school: PlanningSchoolKeyAddInfo):
        # print(planning_school)
        # 保存 模型
        res = await self.planning_school_rule.add_planning_school(planning_school)
        resc = PlanningSchoolCommunications(id=0)
        # logging.debug(resc,'模型2', res.id, type( res.id ))
        newid = str(res.id)
        print(resc, '模型23', res.id, type(res.id))
        # str( res.id).copy()

        resc.planning_school_id = int(newid)
        print(resc, newid, '||||||||')

        # 保存通信信息
        res_comm = await self.planning_school_communication_rule.add_planning_school_communication(resc,
                                                                                                   convertmodel=False)
        print(res_comm, '模型2 res')
        #
        resedu = PlanningSchoolEduInfo(id=0)
        resedu.planning_school_id = res.id
        # 保存教育信息
        res_edu = await self.planning_school_eduinfo_rule.add_planning_school_eduinfo(resedu, convertmodel=False)
        print(res_edu)

        return res

    # # 修改 关键信息
    async def put_keyinfo(self,
                          planning_school: PlanningSchoolKeyInfo,
                          # planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),

                          ):
        # print(planning_school)
        # # 创建类的实例
        # planning_school_key_info = PlanningSchoolKeyInfo()
        # print(planning_school_key_info.__fields__)
        #
        # # 提取每个属性里 title 后面的值
        # titles = {attr: planning_school_key_info.__fields__[attr].title for attr in planning_school_key_info.__fields__}
        #
        # print(titles)

        origin = await self.planning_school_rule.get_planning_school_by_id(planning_school.id)

        res2 = await self.planning_school_rule.compare_modify_fields(planning_school,origin)
        # print(  res2)

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school)



        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res_op = await self.operation_record_rule.add_operation_record(OperationRecord(
            action_target_id=str(planning_school.id),
            operator='admin',
            module=OperationModule.KEYINFO.value,
            target=OperationTargetType.PLANNING_SCHOOL.value,

            action_type=OperationType.MODIFY.value,
            ip='127.0.0.1',
            change_data= str(planning_school)[ 0:250 ],
            change_field='关键信息',
            change_item='关键信息',
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action_reason='修改基本信息',
            doc_upload='',
            status='1',
           account='',))

        return res

    # 删除
    async def delete(self, planning_school_id: int = Query(..., title="", description="学校id/园所id",
                                                           example='2203'), ):
        print(planning_school_id)
        res = await self.planning_school_rule.softdelete_planning_school(planning_school_id)

        return res

    # 修改 变更 基本信息
    async def patch_baseinfo(self, planning_school_baseinfo: PlanningSchoolBaseInfo, ):
        # print(planning_school_baseinfo,type( planning_school_baseinfo))
        res = await self.planning_school_rule.update_planning_school_byargs(planning_school_baseinfo, 2)

        return res

    async def page(self,
                   # page_search: PlanningSchoolPageSearch = Depends(PlanningSchoolPageSearch),
                   block: str = Query("", title=" ", description="地域管辖区", ),
                   planning_school_code: str = Query("", title="", description=" 园所标识码", ),
        planning_school_level: str = Query("", title="", description=" 学校星级", ),
    planning_school_name: str = Query("", title="学校名称", description="1-20字符",),
    planning_school_no:str= Query("", title="学校编号", description="学校编号/园所代码",min_length=1,max_length=20,),
    borough:str=Query("", title="  ", description=" 行政管辖区", ),
    status: PlanningSchoolStatus = Query("", title="", description=" 状态",examples=['正常']),

                   founder_type: List[ PlanningSchoolFounderType]  = Query([], title="", description="举办者类型",examples=['地方']),
                   founder_type_lv2:  List[ str] = Query([], title="", description="举办者类型二级",examples=['教育部门']),
                   founder_type_lv3:  List[ str] = Query([], title="", description="举办者类型三级",examples=['县级教育部门']),

                   page_request=Depends(PageRequest) ):
        print(page_request,)
        items = []
        # exit(1)
        # return page_search
        paging_result = await self.planning_school_rule.query_planning_school_with_page(page_request,planning_school_name,planning_school_no,planning_school_code,
                                                                                        block,planning_school_level,borough,status,founder_type,
                                                                                        founder_type_lv2,
                                                                                        founder_type_lv3

                                                                                        )
        return paging_result

        # return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10, per_page=page_request.per_page, total=100, items=items)

    # 开办 todo 校验合法性等  业务逻辑   开班式 校验所有的数据是否 都填写了
    async def patch_open(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                               min_length=1, max_length=20, example='SC2032633')):
        # print(planning_school)
        planning_school , extra_model= await self.planning_school_rule.get_planning_school_by_id(planning_school_id,PlanningSchoolBaseInfo)
        # planning_school_communication = await self.planning_school_communication_rule.get_planning_school_communication_by_planning_shcool_id(
        #     planning_school_id)
        # planning_school_eduinfo = await self.planning_school_eduinfo_rule.get_planning_school_eduinfo_by_planning_school_id(
        #     planning_school_id)
        print(extra_model)
        print(44444)
        try:
            validated_data = PlanningSchoolBaseInfo.validate(extra_model.dict())
        except Exception as e:
            # 处理验证错误，例如返回错误信息或抛出自定义异常
            # error_messages = ", ".join([f"{k}: {v}" for k, v in e.errors()])
            print(e)
            raise PlanningSchoolValidateError()
        else:
            pass
            # return validated_data


        res = await self.planning_school_rule.update_planning_school_status(planning_school_id,
                                                                            PlanningSchoolStatus.NORMAL.value,'open')

        return res

    # 关闭  todo  附件 和 原因的保存 到日志 
    async def patch_close(self, planning_school_id: str = Query(..., title="学校编号", description="学校id/园所id",
                                                                min_length=1, max_length=20, example='SC2032633'),
                          action_reason: str = Query(None, description="原因", min_length=1, max_length=20,
                                                     example='家庭搬迁'),
                          related_license_upload: List[str] = Query(None, description="相关证照上传", min_length=1,
                                                                    max_length=60, example=''),

                          ):
        # print(planning_school)
        res = await self.planning_school_rule.update_planning_school_status(planning_school_id,
                                                                            PlanningSchoolStatus.CLOSED.value)

        return res

    # 导入 todo 任务队列的
    async def importing(self, planning_school: PlanningSchool):
        print(planning_school)
        return planning_school

    #
    # async def get_extinfo(self):
    #     #
    #     return [ ]
    # 新增 通信信息
    # async def post_comminfo(self,
    #               planning_school: PlanningSchoolCommunications,
    #               # planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),
    #
    #               ):
    #     # print(planning_school)
    #
    #     res = await self.planning_school_communication_rule.add_planning_school_communication(planning_school)
    #
    #     # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
    #
    #     return res

    # 新增 教学信息
    # async def post_eduinfo(self,
    #                         planning_school: PlanningSchoolEduInfo,
    #                         # planning_school_id:str= Query(..., title="学校编号", description="学校id/园所id",min_length=1,max_length=20,example='SC2032633'),
    #
    #                         ):
    #     # print(planning_school)
    #
    #     res = await self.planning_school_eduinfo_rule.add_planning_school_eduinfo(planning_school)
    #
    #     # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
    #
    #     return res

    # 更新 全部信息 用于页面的 暂存 操作  不校验 数据的合法性  todo  允许 部分 不填  现保存
    async def put(self,

                  planning_school: PlanningSchoolBaseInfoOptional,
                  planning_school_communication: PlanningSchoolCommunications,
                  planning_school_eduinfo: PlanningSchoolEduInfo,
                  planning_school_id: int = Query(..., title="", description="学校id/园所id", example='38'),

                  ):
        # print(planning_school)
        planning_school.id = planning_school_id
        planning_school_communication.planning_school_id = planning_school_id
        planning_school_eduinfo.planning_school_id = planning_school_id
        planning_school_communication.id = None
        planning_school_eduinfo.id = None

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school)
        res_com = await self.planning_school_communication_rule.update_planning_school_communication_byargs(
            planning_school_communication)
        res_edu = await self.planning_school_eduinfo_rule.update_planning_school_eduinfo_byargs(planning_school_eduinfo)

        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入

        return res

    # 正式开办  传全部  插入或者更新  todo
    async def put_open(self,

                  planning_school: PlanningSchoolBaseInfo,
                  planning_school_communication: PlanningSchoolCommunications,
                  planning_school_eduinfo: PlanningSchoolEduInfo,
                  planning_school_id: int = Query(..., title="", description="学校id/园所id", example='38'),

                  ):
        # print(planning_school)
        planning_school.id = planning_school_id
        planning_school_communication.planning_school_id = planning_school_id
        planning_school_eduinfo.planning_school_id = planning_school_id
        planning_school_communication.id = None
        planning_school_eduinfo.id = None

        res = await self.planning_school_rule.update_planning_school_byargs(planning_school)
        res_com = await self.planning_school_communication_rule.update_planning_school_communication_byargs(
            planning_school_communication)
        res_edu = await self.planning_school_eduinfo_rule.update_planning_school_eduinfo_byargs(planning_school_eduinfo)

        # todo 记录操作日志到表   参数发进去   暂存 就 如果有 则更新  无则插入
        res2= await self.patch_open(str(planning_school_id))

        return res2

    async def get_search(self,
                     planning_school_name: str = Query("", title="学校名称", description="1-20字符",),

                     page_request=Depends(PageRequest) ):
        print(page_request,)
        items = []
        # exit(1)
        # return page_search
        paging_result = await self.planning_school_rule.query_planning_schools(planning_school_name)
        return paging_result

