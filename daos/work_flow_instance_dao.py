from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.work_flow_define import WorkFlowDefine
from models.work_flow_instance import WorkFlowInstance
from models.work_flow_node_instance import WorkFlowNodeInstance
from typing import List


class WorkFlowInstanceDAO(DAOBase):

    async def add_work_flow_instance(self, work_flow_instance: WorkFlowInstance):
        try:
            session = await self.master_db()
            session.add(work_flow_instance)
            await session.commit()
            await session.refresh(work_flow_instance)
            return work_flow_instance
        except Exception as e:
            raise e

    async def get_work_flow_instance_by_process_instance_id(self, process_instance_id):
        session = await self.slave_db()
        stmt = select(WorkFlowInstance).where(WorkFlowInstance.process_instance_id == process_instance_id)
        result = await session.execute(stmt)
        return result.one_or_none()

    # 更新工作流实例
    async def update_work_flow_instance(self, work_flow_instance: WorkFlowInstance, *args, is_commit: bool = True):
        session = await self.master_db()
        update_contents = get_update_contents(work_flow_instance, *args)
        query = update(WorkFlowInstance).where(
            WorkFlowInstance.process_instance_id == work_flow_instance.process_instance_id).values(**update_contents)
        return await self.update(session, query, work_flow_instance, update_contents, is_commit=is_commit)


