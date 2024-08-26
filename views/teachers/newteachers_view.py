from fastapi import Query, Depends, Body
from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task.task import Task
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.request_context import request_context_manager
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.views import BaseView
from starlette.requests import Request

from common.decorators import require_role_permission
from rules.common.common_rule import get_org_center_user_info
from rules.teacher_import_rule import TeacherImportRule
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule
from rules.teachers_info_rule import TeachersInfoRule
from rules.teachers_rule import TeachersRule
from views.common.common_view import get_extend_params
from views.models.system import UnitType
from views.models.teachers import NewTeacher
from views.models.teachers import Teachers, TeachersCreatModel, CurrentTeacherInfoSaveModel, \
    TeacherInfoSaveModel, TeacherInfoSubmit, CurrentTeacherQuery, \
    TeacherApprovalQuery, TeacherChangeLogQueryModel


class NewTeachersView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_info_rule = get_injector(TeachersInfoRule)
        self.teacher_work_flow_instance_rule = get_injector(TeacherWorkFlowRule)
        self.teacher_import_rule = get_injector(TeacherImportRule)

    # 新增教职工登记信息
    @require_role_permission("newTeacherEntry", "entry")
    async def post_newteacher(self, teachers: TeachersCreatModel):
        print(teachers)
        user_id = request_context_manager.current().current_login_account.name
        res, teacher_base_id = await self.teacher_rule.add_teachers(teachers, user_id)
        result = {}
        result.update(res)
        result.update({"teacher_base_id": teacher_base_id})
        return result

    @require_role_permission("newTeacherEntry", "delete")
    async def delete_newteacher(self, teacher_id: int | str = Query(..., title="教师编号", description="教师编号")):
        """
        删除教师信息
        """
        user_id = request_context_manager.current().current_login_account.name
        teacher_id = int(teacher_id)
        await self.teacher_rule.delete_teachers(teacher_id, user_id)
        return str(teacher_id)

    @require_role_permission("newTeacherEntry", "view")
    # 查询单个教职工登记信息
    async def get_newteacher(self, teacher_id: int | str = Query(..., title="教师编号", description="教师编号")):

        teacher_id = int(teacher_id)
        res = await self.teacher_rule.get_teachers_by_id(teacher_id)
        return res

    @require_role_permission("newTeacherEntry", "edit")
    # 编辑新教职工登记信息
    async def put_newteacher(self, teachers: Teachers):
        print(teachers)
        user_id = request_context_manager.current().current_login_account.name
        res = await self.teacher_rule.update_teachers(teachers, user_id)
        return res

    # 分页查询
    @require_role_permission("newTeacherEntry", "view")
    async def page(self, request: Request, new_teacher=Depends(NewTeacher), page_request=Depends(PageRequest)):
        """
        分页查询
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.unit_type == UnitType.SCHOOL.value:
            new_teacher.teacher_employer = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            extend_param["borough"] = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        paging_result = await self.teacher_info_rule.query_teacher_with_page(new_teacher, page_request, extend_param)
        return paging_result

    # 新教职工基本信息的功能
    # 新增教职工基本信息
    @require_role_permission("newTeacherEntry", "entry")
    async def post_newteacherinfosave(self, teacher_info: TeacherInfoSaveModel):
        """
        保存不经过验证
        """
        user_id = request_context_manager.current().current_login_account.name
        res = await self.teacher_info_rule.update_teachers_info_save(teacher_info, user_id)

        return res

    @require_role_permission("newTeacherEntry", "view")
    async def get_newteacherinfo(self, teacher_id: int | str = Query(..., title="姓名", description="教师名称",
                                                                     example=123)):
        # todo:重新获取时需要根据状态判断一下返回的应该是需要进行验证的还是不需要验证的。
        teacher_id = int(teacher_id)
        res = await self.teacher_info_rule.get_teachers_info_by_teacher_id(teacher_id)
        return res

    # async def put_newteacherinfosubmit(self, teacher_info: TeacherInfoSubmit):
    #     if teacher_info.teacher_base_id > 0:
    #         res = await self.teacher_info_rule.update_teachers_info(teacher_info)
    #     else:
    #         res = await self.teacher_info_rule.add_teachers_info_valid(teacher_info)
    #     return res
    @require_role_permission("newTeacherEntry", "edit")
    async def put_newteacherinforesave(self, teacher_info: CurrentTeacherInfoSaveModel):
        user_id = request_context_manager.current().current_login_account.name
        res = await self.teacher_info_rule.update_teachers_info_save(teacher_info, user_id)
        return res

    async def page_teacher_operation_record_with_page(self, query_model=Depends(TeacherChangeLogQueryModel),
                                                      page_request=Depends(PageRequest)):
        res = await self.teacher_rule.query_teacher_operation_record_with_page(query_model, page_request)
        return res

    # 编辑教职工基本信息
    @require_role_permission("newTeacherEntry", "edit")
    async def put_newteacherinfo(self, teacher_info: TeacherInfoSubmit):
        user_id = request_context_manager.current().current_login_account.name
        if teacher_info.teacher_base_id < 0:
            res = await self.teacher_info_rule.add_teachers_info_valid(teacher_info, user_id)
        else:
            res = await self.teacher_info_rule.update_teachers_info(teacher_info, user_id)
        return res

    # 删除教职工基本信息
    # async def delete_newteacherinfo(self,
    #                                 teacher_id: int = Query(..., title="教师编号", description="教师编号",example=123)):
    #     res = await self.teacher_info_rule.delete_teachers_info(teacher_id)
    #     return res

    # async def patch_submitting(self,
    #                            teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
    #     await self.teacher_rule.submitting(teacher_id)
    #     return teacher_id
    #
    # async def patch_submitted(self,
    #                           teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123)):
    #     await self.teacher_rule.submitted(teacher_id)
    #     return teacher_id
    @require_role_permission("newTeacherApproval", "approval")
    async def patch_entry_approved(self,
                                   teacher_id: int | str = Body(..., title="教师编号", description="教师编号",
                                                                example=123),
                                   process_instance_id: int | str = Body(..., title="流程实例id",
                                                                         description="流程实例id",
                                                                         example=123),
                                   reason: str = Body(None, title="审批意见", description="审批意见", example="同意")):
        user_id = request_context_manager.current().current_login_account.name
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        reason = reason
        return await self.teacher_rule.entry_approved(teacher_id, process_instance_id, user_id, reason)

    @require_role_permission("newTeacherApproval", "reject")
    async def patch_entry_rejected(self,
                                   teacher_id: int | str = Body(..., title="教师编号", description="教师编号",
                                                                example=123),
                                   process_instance_id: int | str = Body(..., title="流程实例id",
                                                                         description="流程实例id",
                                                                         example=123),
                                   reason: str = Body("", title="reason",
                                                      description="审核理由")):
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        user_id = request_context_manager.current().current_login_account.name
        reason = reason
        return await self.teacher_rule.entry_rejected(teacher_id, process_instance_id, user_id, reason)

    @require_role_permission("newTeacherApproval", "revoke")
    async def patch_entry_revoked(self,
                                  teacher_id: int | str = Body(..., title="教师编号", description="教师编号",
                                                               example=123),
                                  process_instance_id: int | str = Body(..., title="流程实例id",
                                                                        description="流程实例id",
                                                                        example=123),
                                  ):
        """
        撤回
        """
        teacher_id = int(teacher_id)
        process_instance_id = int(process_instance_id)
        user_id = request_context_manager.current().current_login_account.name
        return await self.teacher_rule.entry_revoked(teacher_id, process_instance_id, user_id)

    # async def patch_info_submitting(self,
    #                                 teacher_base_id: int = Query(..., title="教师基本信息编号",
    #                                                              description="教师基本信息编号",
    #                                                              example=123)):
    #     await self.teacher_info_rule.submitting(teacher_base_id)
    #     return teacher_base_id

    # async def patch_info_submitted(self,
    #                                teacher_base_id: int = Query(..., title="教师基本信息编号",
    #                                                             description="教师基本信息编号",
    #                                                             example=123)):
    #     await self.teacher_info_rule.submitted(teacher_base_id)
    #     return teacher_base_id

    # async def patch_info_approved(self,
    #                               teacher_base_id: int = Query(..., title="教师基本信息编号",
    #                                                            description="教师基本信息编号",
    #                                                            example=123)):
    #     await self.teacher_info_rule.approved(teacher_base_id)
    #     return teacher_base_id
    #
    # async def patch_info_rejected(self,
    #                               teacher_base_id: int = Query(..., title="教师基本信息编号",
    #                                                            description="教师基本信息编号",
    #                                                            example=123)):
    #     await self.teacher_info_rule.rejected(teacher_base_id)
    #     return teacher_base_id
    @require_role_permission("newTeacherEntry", "importBaseInfo")
    async def post_new_teacher_import(self, file_id: int | str = Query(..., title="文件id",
                                                                       example=123)) -> Task:

        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(
            task_type="teacher_import",
            payload=filestorage,
            # operator="123456"
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    @require_role_permission("newTeacherEntry", "importQuick")
    async def post_new_teacher_save_import(self, file_id: int | str = Query(..., title="文件id",
                                                                            example=123)) -> Task:
        filestorage = await self.teacher_rule.get_task_model_by_id(file_id)
        task = Task(
            task_type="school_task_teacher_save_import",
            payload=filestorage,
            # operator="123456"
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    async def post_new_teacher_export(self, teacher_query: CurrentTeacherQuery) -> Task:
        task = Task(
            task_type="school_task_teacher_export",
            payload=teacher_query,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    @require_role_permission("newTeacherApproval", "view")
    async def page_new_teacher_launch(self, request: Request, teacher_approval_query=Depends(TeacherApprovalQuery),
                                      page_request=Depends(PageRequest)):
        """
        分页查询
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.unit_type == UnitType.SCHOOL.value:
            teacher_approval_query.teacher_employer = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            extend_param["borough"] = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        type = 'launch'
        paging_result = await self.teacher_rule.query_teacher_approval_with_page(type, teacher_approval_query,
                                                                                 page_request, extend_param)
        return paging_result

    @require_role_permission("newTeacherApproval", "view")
    async def page_new_teacher_approval(self, request: Request, teacher_approval_query=Depends(TeacherApprovalQuery),
                                        page_request=Depends(PageRequest)):
        """
        分页查询
        """
        extend_param = {}
        ob = await get_extend_params(request)
        if ob.unit_type == UnitType.SCHOOL.value:
            teacher_approval_query.teacher_employer = ob.school_id
        elif ob.unit_type == UnitType.COUNTRY.value:
            extend_param["borough"] = ob.county_id
        extend_param["applicant_name"] = request_context_manager.current().current_login_account.name
        type = 'approval'
        paging_result = await self.teacher_rule.query_teacher_approval_with_page(type, teacher_approval_query,
                                                                                 page_request, extend_param)
        return paging_result

    # 下面都是测试工作流的

    #
    # async def get_teacher_work_flow_current_node(self, process_instance_id: int = Query(..., title="流程实例id",
    #                                                                                     description="流程实例id")):
    #     res = await self.teacher_work_flow_instance_rule.get_teacher_work_flow_current_node(process_instance_id)
    #     return res
    #
    # async def post_teacher_work_flow(self, teachers: TeachersCreatModel):
    #     parameters = {"process_code": "t_transfer_out", "applicant_name": "张三"}
    #     res = await self.teacher_work_flow_instance_rule.add_teacher_work_flow(teachers, parameters)
    #     return res
    #
    # async def page_query_new_entry_teacher(self, query_model=Depends(NewTeacher), page_request=Depends(PageRequest)):
    #     """
    #     分页查询
    #     """
    #     parameters = {"process_code": "t_transfer_out"}
    #     query_re_model = NewTeacher
    #     paging_result = await self.teacher_work_flow_instance_rule.query_work_flow_instance_with_page(page_request,
    #                                                                                                   query_model,query_re_model, parameters)
    #     return paging_result
    # async def delete_teacher_save_work_flow_instance(self, teacher_id: int = Query(..., title="教师id",
    #                                                                                description="教师id")):
    #     res = await self.teacher_work_flow_instance_rule.delete_teacher_save_work_flow_instance(teacher_id)
    #     return res
    #
    # async def post_process_work_flow_node_instance(self, node_instance_id: int = Query(..., title="流程实例id", description="流程实例id",
    #                                                           example=123), reason: str = Query("", title="reason",
    #                                                                                             description="审核理由")):
    #     parameters = {"user_id": "1243ewrwe", "action": "approved", "description": reason}
    #     res=await self.teacher_work_flow_instance_rule.process_transaction_work_flow(node_instance_id, parameters)

    # async def patch_work_flow_status_by_params(self, process_instance_id: int = Query(..., title="流程实例id",
    #                                                                                   description="流程实例id"),
    #                                            ):
    #     params = {"teacher_main_status": "unemployed", "teacher_sub_status": "unsubmitted"}
    #     await self.teacher_work_flow_instance_rule.update_work_flow_by_param(process_instance_id, params)

    # 测试导入
    async def post_teacher_import_test(self, file_id: int = Query(..., title="文件id", description="文件id")):
        await self.teacher_import_rule.import_teachers_test(file_id)

    async def get_teachers_arg_by_id_test(self,
                                          teacher_id: int | str = Query(..., title="教师编号", description="教师编号",
                                                                        example=123)):
        teacher_id = int(teacher_id)
        res = await self.teacher_rule.send_teacher_to_org_center(teacher_id)
        return res

    async def post_teacher_organization_members_test(self, teacher_id: int | str = Query(..., title="教师编号",
                                                                                         description="教师编号",
                                                                                         example="7210418530586595328"), ):
        teacher_id_list = [
            "7225415333455204352",
            "7225415333622976512",
            "7225415333807525888",
            "7225415333983686656",
            "7225415334147264512",
            "7225415334310842368",
            "7225415334495391744",
            "7225415334654775296",
            "7225415334826741760",
            "7225415334994513920",
            "7225415335149703168",
            "7225415335300698112",
            "7225415335464275968",
            "7225415335619465216",
            "7225415335783043072",
            "7225415335946620928",
            "7225415336118587392",
            "7225415336290553856",
            "7225415336441548800",
            "7225415336609320960",
            "7225415336781287424",
            "7225415336928088064",
            "7225415337146191872",
            "7225415337322352640",
            "7225415337490124800",
            "7225415337687257088",
            "7225415337846640640",
            "7225415338018607104",
            "7225415338219933696",
            "7225415338396094464",
            "7225415338593226752",
            "7225415338811330560",
            "7225415338979102720",
            "7225415339146874880",
            "7225415339314647040",
            "7225415339486613504",
            "7225415339641802752",
            "7225415339805380608",
            "7225415339977347072",
            "7225415340157702144",
            "7225415340317085696",
            "7225415340497440768",
            "7225415340661018624",
            "7225415340812013568",
            "7225415340983980032",
            "7225415341155946496",
            "7225415341311135744",
            "7225415341512462336",
            "7225415341684428800",
            "7225415341831229440",
            "7225415342011584512",
            "7225415342162579456",
            "7225415342380683264",
            "7225415342586204160",
            "7225415342758170624",
            "7225415342917554176",
            "7225415343097909248",
            "7225415343341178880",
            "7225415343873855488",
            "7225415344041627648",
            "7225415344221982720",
            "7225415344385560576",
            "7225415344553332736",
            "7225415344721104896",
            "7225415344888877056",
            "7225415345069232128",
            "7225415345266364416",
            "7225415345421553664",
            "7225415345601908736",
            "7225415345778069504",
            "7225415345950035968",
            "7225415346163945472",
            "7225415346327523328",
            "7225415346512072704",
            "7225415346772119552",
            "7225415346948280320",
            "7225415347103469568",
            "7225415347271241728",
            "7225415347472568320",
            "7225415347657117696",
            "7225415347933941760",
            "7225415348143656960",
            "7225415348315623424",
            "7225415348475006976",
            "7225415348651167744",
            "7225415348823134208",
            "7225415348982517760",
            "7225415349154484224",
            "7225415349322256384",
            "7225415349481639936",
            "7225415349620051968",
            "7225415349783629824",
            "7225415349951401984",
            "7225415350140145664",
            "7225415350312112128",
            "7225415350484078592",
            "7225415350647656448",
            "7225415350811234304",
            "7225415350979006464",
            "7225415351138390016",
            "7225415351297773568",
            "7225415351444574208",
            "7225415351591374848",
            "7225415351780118528",
            "7225415351939502080",
            "7225415352115662848",
            "7225415352279240704",
            "7225415352438624256",
            "7225415352769974272",
            "7225415355672432640",
            "7225415356188332032",
            "7225415356498710528",
            "7225415356712620032",
            "7225415356876197888",
            "7225415357043970048",
            "7225415357203353600",
            "7225415357375320064",
            "7225415357534703616",
            "7225415357694087168",
            "7225415357866053632",
            "7225415358033825792",
            "7225415358180626432",
            "7225415358373564416",
            "7225415358549725184",
            "7225415358709108736",
            "7225415358860103680",
            "7225415359036264448",
            "7225415359191453696",
            "7225415359359225856",
            "7225415359506026496",
            "7225415359661215744",
            "7225415359841570816",
            "7225415359996760064",
            "7225415360164532224",
            "7225415360323915776",
            "7225415360487493632",
            "7225415360651071488",
            "7225415360827232256",
            "7225415360999198720",
            "7225415361162776576",
            "7225415361334743040",
            "7225415361494126592",
            "7225415361653510144",
            "7225415361804505088",
            "7225415361955500032",
            "7225415362173603840",
            "7225415362349764608",
            "7225415362521731072",
            "7225415362689503232",
            "7225415362857275392",
            "7225415363016658944",
            "7225415363176042496",
            "7225415363322843136",
            "7225415363490615296",
            "7225415363645804544",
            "7225415363817771008",
            "7225415363972960256",
            "7225415364157509632",
            "7225415364321087488",
            "7225415364509831168",
            "7225415364685991936",
            "7225415364916678656",
            "7225415365105422336",
            "7225415365327720448",
            "7225415365516464128",
            "7225415365688430592",
            "7225415365852008448",
            "7225415366023974912",
            "7225415366191747072",
            "7225415366351130624",
            "7225415366527291392",
            "7225415366678286336",
            "7225415366858641408",
            "7225415367156436992",
            "7225415367366152192",
            "7225415367550701568",
            "7225415367718473728",
            "7225415367869468672",
            "7225415368037240832",
            "7225415368196624384",
            "7225415368364396544",
            "7225415368527974400",
            "7225415368695746560",
            "7225415368863518720",
            "7225415369027096576",
            "7225415369186480128",
            "7225415369345863680",
            "7225415369496858624",
            "7225415369643659264",
            "7225415369798848512",
            "7225415369958232064",
            "7225415370134392832",
            "7225415370285387776",
            "7225415370436382720",
            "7225415370587377664",
            "7225415370734178304",
            "7225415370906144768",
            "7225415371065528320",
            "7225415371229106176",
            "7225415371413655552",
            "7225415371573039104",
            "7225415371728228352",
            "7225415371883417600",
            "7225415372026023936",
            "7225415372223156224",
            "7225415372395122688",
            "7225415372567089152",
            "7225415372730667008",
            "7225415372894244864",
            "7225415373062017024",
            "7225415373250760704",
            "7225415373473058816",
            "7225415373670191104",
            "7225415373884100608",
            "7225415374089621504",
            "7225415374253199360",
            "7225415374425165824",
            "7225415374601326592",
            "7225415374773293056",
            "7225415374924288000",
            "7225415375087865856",
            "7225415375247249408",
            "7225415375394050048",
            "7225415375549239296",
            "7225415375712817152",
            "7225415375893172224",
            "7225415376098693120",
            "7225415376258076672",
            "7225415376430043136",
            "7225415376597815296",
            "7225415376757198848",
            "7225415377004662784",
            "7225415377151463424",
            "7225415377336012800",
            "7225415377503784960",
            "7225415377788997632",
            "7225415378078404608",
            "7225415378258759680",
            "7225415378455891968",
            "7225415378632052736",
            "7225415378795630592"
        ]
        teacher_id_list_test=["1680801985629900801"]

        for teacher_id in teacher_id_list_test:
            try:
                await self.teacher_rule.add_teacher_organization_members(teacher_id)
            except Exception as e:
                print(f'编号{teacher_id}的发生错误{e}')
                return f'编号{teacher_id}的发生错误{e}'
                # res = await self.teacher_rule.add_teacher_organization_members(teacher_id)

    async def get_send_user_department_to_org_center(self, teacher_id: int | str = Query(..., title="教师编号",
                                                                                         description="教师编号",
                                                                                         example="7210418530586595328"),
                                                     user_id=Query(..., title="教师编号",
                                                                   description="教师编号",
                                                                   example="7210418530586595328")):
        res = await self.teacher_rule.send_user_department_to_org_center(teacher_id, user_id)
        return res

    async def get_account_info_test(self):
        user_info = await get_org_center_user_info()
        return user_info

    async def get_import_teachers_save_test(self):
        result = await self.teacher_import_rule.import_teachers_save_test()
        return result
