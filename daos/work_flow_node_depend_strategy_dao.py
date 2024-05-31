from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.work_flow_node_depend_strategy import WorkFlowNodeDependStrategy

from typing import List


class WorkFlowNodeDependStrategyDAO(DAOBase):

    async def add_work_flow_node_depend_strategy(self, db_records: List[WorkFlowNodeDependStrategy]):
        session = await self.master_db()
        for work_flow_node_depend_strategy in db_records:
            session.add(work_flow_node_depend_strategy)
        await session.commit()
        for work_flow_node_depend_strategy in db_records:
            await session.refresh(work_flow_node_depend_strategy)
        return db_records
