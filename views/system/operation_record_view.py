from mini_framework.web.views import BaseView

from views.models.planning_school import PlanningSchool, PlanningSchoolBaseInfo
from views.models.school import School
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from views.models.operation_record import OperationRecord


# 当前工具包里支持get  patch前缀的 方法的自定义使用
class OperationRecordView(BaseView):

    async def page(self,
                   page_request=Depends(PageRequest),
                   # planning_school_no:str= Query(None, title="学校编号", description="学校编号",min_length=1,max_length=20,example='SC2032633'),

                   ):
        print(page_request)
        items = []

        res = OperationRecord(action_target_id='1', action_type='1', ip='1', change_data='1', change_field='1',
                              change_item='1', timestamp='1', action_reason='1', doc_upload='1', status='1',
                              account='1', operator='1', module='1', target='1' )
        for i in range(0, 1):
            items.append(res)
        print(items)

        return PaginatedResponse(has_next=True, has_prev=True, page=page_request.page, pages=10,
                                 per_page=page_request.per_page, total=100, items=items)
