from sqlalchemy import select
from mini_framework.databases.entities.dao_base import DAOBase

from drop.work_flow_node_define import WorkFlowNodeDefine
from drop.work_flow_define import WorkFlowDefine
from typing import List


class WorkFlowNodeDefineDAO(DAOBase):

    async def add_work_flow_node_define(self, db_records: List[WorkFlowNodeDefine]):
        session = await self.master_db()
        for work_flow_node_define in db_records:
            session.add(work_flow_node_define)
        await session.commit()
        for work_flow_node_define in db_records:
            await session.refresh(work_flow_node_define)
        return db_records

    # 利用process_code查询
    async def get_work_flow_node_define_by_process_code(self, process_code):
        session = await self.slave_db()
        query = select(WorkFlowNodeDefine).join(WorkFlowDefine,
                                                WorkFlowDefine.process_code == WorkFlowNodeDefine.process_code).where(
            WorkFlowNodeDefine.process_code == process_code)
        result = await session.execute(query)
        return result.scalars().all()

    #获取第一个节点
    async def get_first_node_by_process_code(self, process_code):
        session = await self.slave_db()
        query = select(WorkFlowNodeDefine).join(WorkFlowDefine,
                                                WorkFlowDefine.process_code == WorkFlowNodeDefine.process_code).where(
            WorkFlowNodeDefine.process_code == process_code).where(WorkFlowNodeDefine.node_code == process_code)
        result = await session.execute(query)
        return result.scalars().first()

    async def get_work_flow_node_define_by_node_code(self, node_code):
        session = await self.slave_db()
        query = select(WorkFlowNodeDefine).where(WorkFlowNodeDefine.node_code == node_code)
        result = await session.execute(query)
        return result.scalar_one_or_none()
