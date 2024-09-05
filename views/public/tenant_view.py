import traceback
from typing import List

from fastapi import Query
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.class_division_records_rule import ClassDivisionRecordsRule
from rules.operation_record import OperationRecordRule
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_rule import StudentsRule
from rules.tenant_rule import TenantRule
from views.models.class_division_records import ClassDivisionRecordsImport
from views.models.system import OrgCenterApiStatus


class TenantView(BaseView):
    """
    新生基本信息
    """

    def __init__(self):
        super().__init__()
        self.tenant_rule = get_injector(TenantRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.class_division_records_rule = get_injector(ClassDivisionRecordsRule)
        self.operation_record_rule = get_injector(OperationRecordRule)

    #  检查  把 租户的 秘钥等都同步进来
    async def get_sync_tenant(self,
                              school_id: int |str= Query(0, title="学校ID", description="学校ID", examples=[1]),


                                            ):
        """

        """
        paging_result = None
        paging_result = await self.tenant_rule.sync_tenant_all( school_id)

        return {"status": OrgCenterApiStatus.SUCCESS.value, "data": paging_result}


