from sqlalchemy import select
from mini_framework.databases.entities.dao_base import DAOBase

from drop.work_flow_node_depend import WorkFlowNodeDepend
from typing import List


class WorkFlowNodeDependDAO(DAOBase):

    async def add_work_flow_node_depend(self, db_records: List[WorkFlowNodeDepend]):
        session = await self.master_db()
        for work_flow_node_depend in db_records:
            session.add(work_flow_node_depend)
        await session.commit()
        for work_flow_node_depend in db_records:
            await session.refresh(work_flow_node_depend)
        return db_records

    #获取依赖关系
    async def get_work_flow_node_depend_by_node_code(self, node_code):
        session = await self.slave_db()
        query = select(WorkFlowNodeDepend).where(WorkFlowNodeDepend.source_node == node_code)
        result = await session.execute(query)
        return result.scalars().all()
