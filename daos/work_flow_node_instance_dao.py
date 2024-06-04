from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.work_flow_define import WorkFlowDefine
from models.work_flow_node_define import WorkFlowNodeDefine
from models.work_flow_instance import WorkFlowInstance
from models.work_flow_node_instance import WorkFlowNodeInstance
from typing import List


class WorkFlowNodeInstanceDAO(DAOBase):

    async def add_work_flow_node_instance(self, work_flow_node_instance: WorkFlowNodeInstance):
        try:
            session = await self.master_db()
            session.add(work_flow_node_instance)
            await session.commit()
            await session.refresh(work_flow_node_instance)
            return work_flow_node_instance
        except Exception as e:
            raise e

    async def get_work_flow_instance_by_node_instance_id(self, node_instance_id):
        session = await self.slave_db()
        stmt = select(WorkFlowNodeInstance).where(WorkFlowNodeInstance.node_instance_id == node_instance_id)
        result = await session.execute(stmt)
        return result.one_or_none()

    async def update_work_flow_node_instance(self, work_flow_node_instance: WorkFlowNodeInstance, *args,
                                             is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(work_flow_node_instance, *args)
        query = update(WorkFlowNodeInstance).where(
            WorkFlowNodeInstance.node_instance_id == work_flow_node_instance.node_instance_id).values(
            **update_contents)
        return await self.update(session, query, work_flow_node_instance, update_contents, is_commit=is_commit)

    async def get_work_flow_node_instance_by_node_code_and_process_instance_id(self, node_code, process_instance_id):
        session = await self.slave_db()
        query = (select(WorkFlowNodeInstance).join(WorkFlowInstance,
                                                   WorkFlowInstance.process_instance_id == WorkFlowNodeInstance.process_instance_id).join(
            WorkFlowNodeDefine, WorkFlowNodeDefine.node_code == WorkFlowNodeInstance.node_code).where(
            WorkFlowNodeInstance.node_code == node_code,
            WorkFlowNodeInstance.process_instance_id == process_instance_id,
            WorkFlowNodeInstance.node_status == "pending"))
        result = await session.execute(query)
        return result.one_or_none
