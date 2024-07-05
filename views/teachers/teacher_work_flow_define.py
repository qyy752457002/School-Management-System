from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from drop.work_flow_define_rule import WorkFlowNodeDefineRule
from views.models.work_flow_define import WorkFlowDefineModel
from views.models.work_flow_instance import WorkFlowInstanceModel


class WorkFlowDefineView(BaseView):
    def __init__(self):
        super().__init__()

        self.work_flow_define_rule = get_injector(WorkFlowNodeDefineRule)
        self.work_flow_instance_rule = get_injector(WorkFlowNodeDefineRule)

    async def post_work_flow_define(self, work_flow_define: WorkFlowDefineModel):
        res = await self.work_flow_define_rule.add_work_flow_define(work_flow_define)
        return res

    async def post_work_flow_instance(self, work_flow_instance: WorkFlowInstanceModel):
        res = await self.work_flow_define_rule.add_work_flow_instance(work_flow_instance)
        return res


