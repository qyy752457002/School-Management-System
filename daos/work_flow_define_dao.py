from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.work_flow_define import WorkFlowDefine

from typing import List


class WorkFlowDefineDAO(DAOBase):

    async def add_work_flow_define(self, work_flow_define: WorkFlowDefine):
        session = await self.master_db()
        session.add(work_flow_define)
        await session.commit()
        await session.refresh(work_flow_define)
        return work_flow_define
