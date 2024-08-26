from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from daos.work_flow_node_define_dao import WorkFlowNodeDefineDAO
from daos.work_flow_node_depend_dao import WorkFlowNodeDependDAO
from daos.work_flow_node_depend_strategy_dao import WorkFlowNodeDependStrategyDAO
from daos.work_flow_instance_dao import WorkFlowInstanceDAO
from daos.work_flow_node_instance_dao import WorkFlowNodeInstanceDAO
from views.models.work_flow_instance import WorkFlowInstanceModel, WorkFlowInstanceCreateModel
from drop.work_flow_instance import WorkFlowInstance
from drop.work_flow_node_instance import WorkFlowNodeInstance
from datetime import datetime


@dataclass_inject
class WorkFlowNodeInstanceRule(object):
    work_flow_instance_dao: WorkFlowInstanceDAO
    work_flow_node_instance_dao: WorkFlowNodeInstanceDAO
    work_flow_node_define_dao: WorkFlowNodeDefineDAO
    work_flow_node_depend_dao: WorkFlowNodeDependDAO
    work_flow_node_depend_strategy_dao: WorkFlowNodeDependStrategyDAO

    async def get_work_flow_instance_by_work_flow_instance_id(self, process_instance_id):
        work_flow_instance_db = await self.work_flow_instance_dao.get_work_flow_instance_by_process_instance_id(
            process_instance_id)
        work_flow_instance = orm_model_to_view_model(work_flow_instance_db, WorkFlowInstanceModel)
        return work_flow_instance

    async def get_work_flow_instance_status_by_work_flow_instance_id(self, process_instance_id):
        work_flow_instance_db = await self.work_flow_instance_dao.get_work_flow_instance_by_process_instance_id(
            process_instance_id)
        work_flow_instance_status = work_flow_instance_db.process_status
        return work_flow_instance_status

    async def get_is_revoke_by_current_node(self, node_code):
        """
        这个是用来判断当前节点是否可以撤回
        """
        depend_code = await self.work_flow_node_depend_strategy_dao.get_depend_code_by_node_code(node_code)
        is_revoke = False
        for code in depend_code:
            result = await self.work_flow_node_depend_strategy_dao.get_is_revoke_by_depend_code(code.depend_code)
            if result:
                is_revoke = True
                return is_revoke
        return is_revoke


    async def add_work_flow_instance(self, work_flow_instance: WorkFlowInstanceCreateModel):
        work_flow_instance_db = view_model_to_orm_model(work_flow_instance, WorkFlowInstance)
        work_flow_instance_db = await self.work_flow_instance_dao.add_work_flow_instance(work_flow_instance_db)
        work_flow_instance = orm_model_to_view_model(work_flow_instance_db, WorkFlowInstanceModel)
        return work_flow_instance

    async def update_work_flow_instance(self, work_flow_instance):
        exists_work_flow_instance_info = await self.work_flow_instance_dao.get_work_flow_instance_by_process_instance_id(
            work_flow_instance.process_instance_id)
        if not exists_work_flow_instance_info:
            raise Exception(f"编号为{work_flow_instance.process_instance_id}的work_flow_instance不存在")
        need_update_list = []
        for key, value in work_flow_instance.dict().items():
            if value:
                need_update_list.append(key)
        work_flow_instance = await self.work_flow_instance_dao.update_work_flow_instance(work_flow_instance,
                                                                                         *need_update_list)
        return work_flow_instance

    # 修改流程状态
    async def flow_rejected(self, process_instance_id):
        process_instance = await self.work_flow_instance_dao.get_work_flow_instance_by_process_instance_id(
            process_instance_id)
        if not process_instance:
            raise Exception(f"编号为{process_instance_id}的work_flow_instance不存在")
        process_instance.process_status = "rejected"
        process_instance.end_time = datetime.now()
        process_instance = await self.work_flow_instance_dao.update_work_flow_instance(process_instance,
                                                                                       "process_status", "end_time")
        return process_instance

    async def flow_approved(self, process_instance_id):
        process_instance = await self.work_flow_instance_dao.get_work_flow_instance_by_process_instance_id(
            process_instance_id)
        if not process_instance:
            raise Exception(f"编号为{process_instance_id}的work_flow_instance不存在")
        process_instance.process_status = "approved"
        process_instance.end_time = datetime.now()
        process_instance = await self.work_flow_instance_dao.update_work_flow_instance(process_instance,
                                                                                       "process_status", "end_time")

        return process_instance

    # 工作节点相关
    # 创建第一个节点
    async def create_first_node_instance(self, work_flow_instance: WorkFlowInstanceModel):
        process_code = work_flow_instance.process_code
        operator_name = work_flow_instance.applicant_name
        process_instance_id = work_flow_instance.process_instance_id
        first_node = await self.work_flow_node_define_dao.get_first_node_by_process_code(process_code)
        node_code = first_node.node_code
        node_instance = WorkFlowNodeInstance(process_instance_id=process_instance_id,
                                             node_code=node_code, node_status="pending",
                                             operator_name=operator_name, action="create", description="")
        node_instance = await self.work_flow_node_instance_dao.add_work_flow_node_instance(node_instance)
        return node_instance

    # 处理当前节点并确定下一个节点
    async def process_current_node(self, node_instance: WorkFlowNodeInstance, parameters: dict):
        operator_id = parameters.get("user_id")
        role = query_role(operator_id)
        has_permission = await self.check_permission(operator_id, role, node_instance)
        if not has_permission:
            raise Exception(f"用户{operator_id}没有权限处理节点{node_instance.node_code}")
        parameters["node.status"] = node_instance.node_status

        # 获取当前节点的依赖关系
        dependencies = await self.work_flow_node_depend_dao.get_work_flow_node_depend_by_node_code(
            node_instance.node_code)
        next_node_instance = None
        if "start" in node_instance.node_code:
            next_node_code = dependencies[0].next_node
            next_node_instance = await self.create_next_node_instance(node_instance, next_node_code)

        else:
            for dependency in dependencies:
                strategies = await self.work_flow_node_depend_strategy_dao.get_work_flow_node_depend_strategy_by_depend_code(
                    dependency.depend_code)
                if all(strategy.parameter_name in parameters and
                       parameters[strategy.parameter_name] == strategy.parameter_value for strategy in strategies):
                    next_node_instance = await self.create_next_node_instance(node_instance, dependency.next_node)
                if next_node_instance:  # 如果找到下一个节点，就不再继续查找
                    break
        node_instance.action = parameters.get("action")
        if node_instance.action != "create":
            node_instance.node_status = "completed"
        else:
            node_instance.node_status = "pending"
        node_instance.operator_time = datetime.now()
        node_instance.operator_id = operator_id
        await self.work_flow_node_instance_dao.update_work_flow_node_instance(node_instance,
                                                                              "node_status", "operator_id",
                                                                              "operator_time", "action")
        # todo 这里应该要记录一下操作日志。
        if "fail" in node_instance.node_code:
            await self.flow_rejected(node_instance.process_instance_id)
        elif "success" in node_instance.node_code:
            await self.flow_approved(node_instance.process_instance_id)
        return next_node_instance

    # 创建下一个节点
    async def create_next_node_instance(self, current_node_instance, next_node_code):
        node_code = next_node_code
        if "start" in next_node_code:
            # 如果是发起方撤回，则直接返回第一个节点，而不是创建新的节点
            process_instance_id = current_node_instance.process_instance_id
            next_node_instance = await self.work_flow_node_instance_dao.get_work_flow_node_instance_by_node_code_and_process_instance_id(
                node_code, process_instance_id)
            return next_node_instance
        next_node_definition = await self.work_flow_node_define_dao.get_work_flow_node_define_by_node_code(
            next_node_code)
        if next_node_definition:
            next_node_instance = WorkFlowNodeInstance(process_instance_id=current_node_instance.process_instance_id,
                                                      node_code=next_node_definition.next_node_code,
                                                      node_status="pending",
                                                      action="create", description="",
                                                      created_time=datetime.now())
            next_node_instance = await self.work_flow_node_instance_dao.add_work_flow_node_instance(next_node_instance)
            return next_node_instance
        return None

    # 流程初始化

    async def initiate_process(self, work_flow_instance: WorkFlowInstanceCreateModel):

        work_flow_instance_db = view_model_to_orm_model(work_flow_instance, WorkFlowInstance)
        work_flow_instance_db = await self.work_flow_instance_dao.add_work_flow_instance(work_flow_instance_db)
        work_flow_instance = orm_model_to_view_model(work_flow_instance_db, WorkFlowInstanceModel)
        first_node_instance = await self.create_first_node_instance(work_flow_instance)
        return work_flow_instance, first_node_instance

    async def get_parameters(self, **kwargs):
        """
        user_id: 操作人id
        action: 操作
        """
        parameters = {}
        for key, value in kwargs.items():
            if value:
                parameters[key] = value
        return parameters

    async def check_permission(self, operator_id, role, node_instance):
        return True


def query_role(user_id):
    pass


def create_work_flow_instance(self, process_code, applicant_name):
    """
    process_code: str = Field(..., title="流程定义id", description="流程定义id")
    applicant_name: str = Field(..., title="申请人姓名", description="申请人姓名")
    start_time: datetime = Field(datetime.now(), title="开始时间", description="开始时间")
    end_time: Optional[datetime] = Field(None, title="结束时间", description="结束时间")
    process_status: WorkFlowInstanceStatus = Field("pending", title="流程状态", description="流程状态")
    description: str = Field("", title="说明", description="说明")
    """
    process_code = process_code
    applicant_name = applicant_name
    work_flow_instance = WorkFlowInstanceCreateModel(process_code=process_code,
                                                     applicant_name=applicant_name,
                                                     start_time=datetime.now(),
                                                     end_time=None,
                                                     process_status="pending",
                                                     description="")
