import traceback
from typing import List

from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView

from rules.class_division_records_rule import ClassDivisionRecordsRule
from rules.operation_record import OperationRecordRule
from rules.students_base_info_rule import StudentsBaseInfoRule
from rules.students_rule import StudentsRule
from views.models.class_division_records import ClassDivisionRecordsImport
from views.models.system import OrgCenterApiStatus


class NewsStudentsInfoView(BaseView):
    """
    新生基本信息
    """

    def __init__(self):
        super().__init__()
        self.students_rule = get_injector(StudentsRule)
        self.students_base_info_rule = get_injector(StudentsBaseInfoRule)
        self.class_division_records_rule = get_injector(ClassDivisionRecordsRule)
        self.operation_record_rule = get_injector(OperationRecordRule)

    # 供阳光分班结果同步
    async def post_newstudent_classdivision(self,
                                            class_division_records: List[ClassDivisionRecordsImport],

                                            ):
        """

        """
        paging_result = None
        paging_result = await self.deal_newstudent_classdivision(class_division_records)
        if paging_result and len(paging_result) >0:
            return {"status": OrgCenterApiStatus.ERROR.value, "data": paging_result}

        # for class_division_record in class_division_records:
        return {"status": OrgCenterApiStatus.SUCCESS.value, "data": paging_result}


    # 修改分班
    async def deal_newstudent_classdivision(self,
                                            class_division_records

                                            ):
        """
        分班 捕获异常
        """
        try:
            res = None
            # 根据编码转换ID 等操作
            res_check = await self.class_division_records_rule.add_class_division_records_and_update_student_baseinfo(class_division_records,True)
            if res_check and len(res_check)>0:
                return res_check
            res = await self.class_division_records_rule.add_class_division_records_and_update_student_baseinfo(class_division_records,)


        except ValueError as e:
            traceback.print_exc()
            return e
        except Exception as e:
            print(e)
            traceback.print_exc()

            return e

        return res
