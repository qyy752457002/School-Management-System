from sqlalchemy import select
from mini_framework.databases.entities.dao_base import DAOBase

from drop.work_flow_define import WorkFlowDefine


class WorkFlowDefineDAO(DAOBase):

    async def add_work_flow_define(self, work_flow_define: WorkFlowDefine):
        try:
            session = await self.master_db()
            session.add(work_flow_define)
            await session.commit()
            await session.refresh(work_flow_define)
            return work_flow_define
        except Exception as e:
            raise e

    # 利用process_code查询
    async def get_work_flow_define_by_process_code(self, process_code):
        session = await self.slave_db()
        stmt = select(WorkFlowDefine).where(WorkFlowDefine.process_code == process_code)
        result = await session.execute(stmt)
        return result.one_or_none()


