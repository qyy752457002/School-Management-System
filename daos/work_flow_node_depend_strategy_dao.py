from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.work_flow_node_depend_strategy import WorkFlowNodeDependStrategy
from models.work_flow_node_depend import WorkFlowNodeDepend
from models.work_flow_node_define import WorkFlowNodeDefine

from typing import List


class WorkFlowNodeDependStrategyDAO(DAOBase):

    # 一次性添加流程/节点/依赖/策略

    async def add_work_flow_process(self, work_flow_define_db, work_flow_node_list: List[WorkFlowNodeDefine],
                                    work_flow_node_depends_list: List[WorkFlowNodeDepend],
                                    work_flow_node_depends_strategy_list: List[
                                        WorkFlowNodeDependStrategy]):
        session = await self.master_db()

        session.add(work_flow_define_db)
        for work_flow_node_define in work_flow_node_list:
            session.add(work_flow_node_define)
        for work_flow_node_depend in work_flow_node_depends_list:
            session.add(work_flow_node_depend)
        for work_flow_node_depend_strategy in work_flow_node_depends_strategy_list:
            session.add(work_flow_node_depend_strategy)
        await session.commit()

        await session.refresh(work_flow_define_db)
        for work_flow_node_define in work_flow_node_list:
            await session.refresh(work_flow_node_define)
        for work_flow_node_depend in work_flow_node_depends_list:
            await session.refresh(work_flow_node_depend)
        for work_flow_node_depend_strategy in work_flow_node_depends_strategy_list:
            await session.refresh(work_flow_node_depend_strategy)
        return work_flow_define_db, work_flow_node_list, work_flow_node_depends_list, work_flow_node_depends_strategy_list

    # 获取策略
    async def get_work_flow_node_depend_strategy_by_depend_code(self, depend_code):
        session = await self.slave_db()
        query = select(WorkFlowNodeDependStrategy).join(WorkFlowNodeDepend,
                                                        WorkFlowNodeDepend.depend_code == WorkFlowNodeDependStrategy.depend_code).where(
            WorkFlowNodeDependStrategy.depend_code == depend_code)
        result = await session.execute(query)
        return result.scalars().all
