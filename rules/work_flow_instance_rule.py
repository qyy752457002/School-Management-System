from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from views.models.work_flow_define import WorkFlowDefineModel
from daos.work_flow_node_define_dao import WorkFlowNodeDefineDAO
from daos.work_flow_define_dao import WorkFlowDefineDAO
from daos.work_flow_node_depend_dao import WorkFlowNodeDependDAO
from daos.work_flow_node_depend_strategy_dao import WorkFlowNodeDependStrategyDAO
from models.work_flow_node_define import WorkFlowNodeDefine
from models.work_flow_node_depend import WorkFlowNodeDepend
from models.work_flow_define import WorkFlowDefine
from models.work_flow_node_depend_strategy import WorkFlowNodeDependStrategy
from mini_framework.databases.entities import BaseDBModel, to_dict
from daos.work_flow_instance_dao import WorkFlowInstanceDAO
from daos.work_flow_node_instance_dao import WorkFlowNodeInstanceDAO
from views.models.work_flow_instance import WorkFlowInstanceModel, WorkFlowInstanceCreateModel, \
    WorkFlowNodeInstanceModel, WorkFlowNodeCreatInstanceModel
from models.work_flow_instance import WorkFlowInstance
from models.work_flow_node_instance import WorkFlowNodeInstance
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

    async def flow_pending(self, process_instance_id):
        process_instance = await self.work_flow_instance_dao.get_work_flow_instance_by_process_instance_id(
            process_instance_id)
        if not process_instance:
            raise Exception(f"编号为{process_instance_id}的work_flow_instance不存在")
        process_instance.process_status = "pending"
        process_instance = await self.work_flow_instance_dao.update_work_flow_instance(process_instance,
                                                                                       "process_status")

        return await self.work_flow_instance_dao.update_work_flow_instance(process_instance, "process_status")

    async def flow_rejected(self, process_instance_id):
        process_instance = await self.work_flow_instance_dao.get_work_flow_instance_by_process_instance_id(
            process_instance_id)
        if not process_instance:
            raise Exception(f"编号为{process_instance_id}的work_flow_instance不存在")
        process_instance.process_status = "rejected"
        process_instance = await self.work_flow_instance_dao.update_work_flow_instance(process_instance,
                                                                                       "process_status")

        return await self.work_flow_instance_dao.update_work_flow_instance(process_instance, "process_status")

    async def flow_approved(self, process_instance_id):
        process_instance = await self.work_flow_instance_dao.get_work_flow_instance_by_process_instance_id(
            process_instance_id)
        if not process_instance:
            raise Exception(f"编号为{process_instance_id}的work_flow_instance不存在")
        process_instance.process_status = "approved"
        process_instance = await self.work_flow_instance_dao.update_work_flow_instance(process_instance,
                                                                                       "process_status")

        return await self.work_flow_instance_dao.update_work_flow_instance(process_instance, "process_status")

    # 工作节点相关
    # 创建第一个节点
    async def create_first_node_instance(self, work_flow_node_instance: WorkFlowInstance):
        process_code = work_flow_node_instance.process_code
        operator_id = work_flow_node_instance.applicant_id
        process_instance_id = work_flow_node_instance.process_instance_id
        first_node = await self.work_flow_node_define_dao.get_first_node_by_process_code(process_code)
        node_code = first_node.node_code
        node_instance = WorkFlowNodeInstance(process_instance_id=process_instance_id,
                                             node_code=node_code, node_status="pending", operator_role="",
                                             operator_id=operator_id, action="create", description="")
        node_instance = await self.work_flow_node_instance_dao.add_work_flow_node_instance(node_instance)
        return node_instance

    # 处理当前节点并确定下一个节点
    async def process_current_node(self, node_instance, action, parameters):
        node_instance.node_status = "completed"
        node_instance.operator_time = datetime.now()
        node_instance.action = action
        node_instance = await self.work_flow_node_instance_dao.update_work_flow_node_instance(node_instance,
                                                                                              "node_status",
                                                                                              "operator_time", "action")

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
                for strategy in strategies:
                    if (strategy.parameter_name in parameters and
                            parameters[strategy.parameter_name] == strategy.parameter_value):
                        next_node_instance = await self.create_next_node_instance(node_instance, dependency.next_node)
                        break
                if next_node_instance:  # 如果找到下一个节点，就不再继续查找
                    break
        return next_node_instance

    # 创建下一个节点
    async def create_next_node_instance(self, current_node_instance, next_node_code):
        next_node_definition = await self.work_flow_node_define_dao.get_work_flow_node_define_by_node_code(
            next_node_code)

