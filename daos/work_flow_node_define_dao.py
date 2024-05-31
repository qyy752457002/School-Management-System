from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.work_flow_node_define import WorkFlowNodeDefine
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
