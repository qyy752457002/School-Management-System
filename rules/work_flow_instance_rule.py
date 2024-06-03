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
from views.models.work_flow_instance import WorkFlowInstanceModel, WorkFlowInstanceCreateModel,WorkFlowNodeInstanceModel,WorkFlowNodeCreatInstanceModel
from models.work_flow_instance import WorkFlowInstance
from models.work_flow_node_instance import WorkFlowNodeInstance


@dataclass_inject
class WorkFlowNodeInstanceRule(object):
    work_flow_instance_dao: WorkFlowInstanceDAO
    work_flow_node_instance_dao: WorkFlowNodeInstanceDAO


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
    async def create_first_node_instance(self, work_flow_node_instance: WorkFlowNodeCreatInstanceModel):
        process_instance_id = work_flow_node_instance.process_instance_id

