from datetime import datetime, date

from mini_framework.web.views import BaseView

from models.public_enum import YesOrNo
from views.models.teachers import NewTeacher
from fastapi import Query, Depends, Body

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.std_models.page import PageRequest, PaginatedResponse
from mini_framework.web.views import BaseView
from rules.teachers_rule import TeachersRule
from views.models.teachers import Teachers, TeacherInfo, TeachersCreatModel, CurrentTeacherInfoSaveModel, \
    TeacherInfoSaveModel, TeacherInfoSubmit, CombinedModel, TeacherFileStorageModel, CurrentTeacherQuery, \
    TeacherApprovalQuery, NewTeacherRe, TeacherChangeLogQueryModel
from rules.teachers_info_rule import TeachersInfoRule
from mini_framework.web.request_context import request_context_manager

from mini_framework.async_task.app.app_factory import app
from mini_framework.async_task.task import Task
from views.models.teachers import NewTeacherTask
from rules.teacher_work_flow_instance_rule import TeacherWorkFlowRule


class NewTeachersView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_rule = get_injector(TeachersRule)
        self.teacher_info_rule = get_injector(TeachersInfoRule)
        self.teacher_work_flow_instance_rule = get_injector(TeacherWorkFlowRule)

    # 新增教职工登记信息
    async def post_newteacher(self, teachers: TeachersCreatModel):
        print(teachers)
        user_id = "asdfasdf"
        res = await self.teacher_rule.add_teachers(teachers, user_id)
        return res

    async def delete_newteacher(self, teacher_id: int = Query(..., title="教师编号", description="教师编号")):
        """
        删除教师信息
        """
        user_id = "asdfasdf"
        await self.teacher_rule.delete_teachers(teacher_id, user_id)
        return str(teacher_id)

    # 查询单个教职工登记信息
    async def get_newteacher(self, teacher_id: int = Query(..., title="教师编号", description="教师编号")):
        res = await self.teacher_rule.get_teachers_by_id(teacher_id)
        return res

    # 编辑新教职工登记信息
    async def put_newteacher(self, teachers: Teachers):
        print(teachers)
        user_id = "asdfasdf"
        res = await self.teacher_rule.update_teachers(teachers, user_id)
        return res

    # 分页查询

    async def page(self, new_teacher=Depends(NewTeacher), page_request=Depends(PageRequest)):
        """
        分页查询
        """
        user_id = "asdfasdf"
        paging_result = await self.teacher_info_rule.query_teacher_with_page(new_teacher, page_request, user_id)
        return paging_result

    # 新教职工基本信息的功能
    # 新增教职工基本信息
    async def post_newteacherinfosave(self, teacher_info: TeacherInfoSaveModel):
        """
        保存不经过验证
        """
        user_id = "asdfasdf"
        exits = await self.teacher_info_rule.get_teachers_info_by_teacher_id_exit(teacher_info.teacher_id)
        print(exits)
        if exits:
            res = await self.teacher_info_rule.update_teachers_info_save(teacher_info, user_id)
        else:
            res = await self.teacher_info_rule.add_teachers_info(teacher_info, user_id)
        return res

    async def get_newteacherinfo(self, teacher_id: int = Query(..., title="教师名称", description="教师名称",
                                                               example=123)):
        # todo:重新获取时需要根据状态判断一下返回的应该是需要进行验证的还是不需要验证的。
        res = await self.teacher_info_rule.get_teachers_info_by_teacher_id(teacher_id)
        return res

    # async def put_newteacherinfosubmit(self, teacher_info: TeacherInfoSubmit):
    #     if teacher_info.teacher_base_id > 0:
    #         res = await self.teacher_info_rule.update_teachers_info(teacher_info)
    #     else:
    #         res = await self.teacher_info_rule.add_teachers_info_valid(teacher_info)
    #     return res

    async def put_newteacherinforesave(self, teacher_info: CurrentTeacherInfoSaveModel):

        res = await self.teacher_info_rule.update_teachers_info_save(teacher_info)
        return res

    async def page_teacher_operation_record_with_page(self, query_model=Depends(TeacherChangeLogQueryModel),
                                                      page_request=Depends(PageRequest)):
        res = await self.teacher_rule.query_teacher_operation_record_with_page(query_model, page_request)
        return res

    # 编辑教职工基本信息
    async def put_newteacherinfo(self, teacher_info: TeacherInfo):
        user_id = "asdfasdf"
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

    async def patch_entry_approved(self,
                                   teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123),
                                   process_instance_id: int = Query(..., title="流程实例id", description="流程实例id",
                                                                    example=123),
                                   reason: str = Query(None, title="审批意见", description="审批意见", example="同意")):
        user_id = "asdfasdf"
        reason = reason
        await self.teacher_rule.entry_approved(teacher_id, process_instance_id, user_id, reason)
        return teacher_id

    async def patch_entry_rejected(self,
                                   teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123),
                                   process_instance_id: int = Query(..., title="流程实例id", description="流程实例id",
                                                                    example=123),
                                   reason: str = Query("", title="reason",
                                                       description="审核理由")):
        user_id = "asdfasdf"
        reason = reason
        await self.teacher_rule.entry_rejected(teacher_id, process_instance_id, user_id, reason)
        return teacher_id

    async def patch_entry_revoked(self,
                                  teacher_id: int = Query(..., title="教师编号", description="教师编号", example=123),
                                  process_instance_id: int = Query(..., title="流程实例id", description="流程实例id",
                                                                   example=123),
                                  ):
        """
        撤回
        """
        user_id = "asdfasdf"
        await self.teacher_rule.entry_revoked(teacher_id, process_instance_id, user_id)
        return teacher_id

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

    async def post_new_teacher_import(self, filestorage: TeacherFileStorageModel) -> Task:

        task = Task(
            task_type="teacher_import",
            payload=filestorage,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    async def post_new_teacher_export(self, teacher_query: CurrentTeacherQuery) -> Task:
        task = Task(
            task_type="teacher_export",
            payload=teacher_query,
            operator=request_context_manager.current().current_login_account.account_id
        )
        task = await app.task_topic.send(task)
        print('发生任务成功')
        return task

    async def page_new_teacher_launch(self, teacher_approval_query=Depends(TeacherApprovalQuery),
                                      page_request=Depends(PageRequest)):
        """
        分页查询
        """
        type = 'launch'
        user_id = "asdfasdf"
        paging_result = await self.teacher_rule.query_teacher_approval_with_page(type, teacher_approval_query,
                                                                                 page_request, user_id)
        return paging_result

    async def page_new_teacher_approval(self, teacher_approval_query=Depends(TeacherApprovalQuery),
                                        page_request=Depends(PageRequest)):
        """
        分页查询
        """
        type = 'approval'
        user_id = "asdfasdf"
        paging_result = await self.teacher_rule.query_teacher_approval_with_page(type, teacher_approval_query,
                                                                                 page_request, user_id)
        return paging_result

    # 下面都是测试工作流的

    # async def get_work_flow_node_log(self, process_instance_id: int = Query(..., title="流程实例id",
    #                                                                         description="流程实例id")):
    #     res = await self.teacher_work_flow_instance_rule.get_teacher_work_flow_log_by(process_instance_id)
    #     return res
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
