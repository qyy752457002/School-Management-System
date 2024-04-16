from typing import List

from mini_framework.web.views import BaseView

from views.models.students import NewStudents, NewStudentsQuery, StudentsKeyinfo, StudentsBaseInfo
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from datetime import date
from views.models.students import StudentEduInfo


class CurrentStudentsView(BaseView):
    # 在校生流出
    async def patch_flowout(self,    student_id: str = Query(...,   description="学生id",min_length=1,max_length=20,example='SC2032633'),
                            flowout_time    :str= Query(..., description="流出时间" ,min_length=1,max_length=20,example='2020-10-10'),
                            flowout_reason   :str= Query(..., description="流出原因" ,min_length=1,max_length=20,example='家庭搬迁'),
                            ):
        # print(new_students_key_info)
        return student_id

    # 在校生转入  todo 届别 班级
    async def patch_transferin(self,StudentEduInfo:StudentEduInfo

                            ):
        # print(new_students_key_info)
        return StudentEduInfo


    # 在校生转入   审批
    async def patch_transferin_audit(self,transferin_audit_id:str=Query(...,   description="转入申请id",min_length=1,max_length=20,example='SC2032633'),

                               ):
        # print(new_students_key_info)
        return transferin_audit_id



    # 在校生转入   系统外转入
    async def patch_transferin_fromoutside(self,StudentEduInfo:StudentEduInfo,
                                           NewStudents:NewStudents,
                                           StudentoutEduInfo:StudentEduInfo,



                               ):
        # print(new_students_key_info)
        return StudentEduInfo


    # 在校生 系统外转出
    async def patch_transferout_tooutside(self,StudentEduInfo:StudentEduInfo,
                                           NewStudents:NewStudents,
                                           StudentoutEduInfo:StudentEduInfo,



                                           ):
        # print(new_students_key_info)
        return StudentEduInfo



    # 在校生转入   审批同意
    async def patch_transferin_auditpass(self,
                                         transferin_audit_id:str=Query(...,   description="转入申请id",min_length=1,max_length=20,example='SC2032633'),
                                         remark:str=Query(...,   description="备注",min_length=1,max_length=20,example='SC2032633'),
                                     ):
        # print(new_students_key_info)
        return transferin_audit_id

    # 在校生转入   审批拒绝
    async def patch_transferin_auditrefuse(self,
                                         transferin_audit_id:str=Query(...,   description="转入申请id",min_length=1,max_length=20,example='SC2032633'),
                                         remark:str=Query(...,   description="备注",min_length=1,max_length=20,example='SC2032633'),
                                         ):
        # print(new_students_key_info)
        return transferin_audit_id



    # 在校生 发起毕业 todo  支持传入部门学生ID或者  / all年级毕业
    async def patch_graduate(self,
                                           student_id: List[str]=Query(...,   description="学生ID",min_length=1,max_length=20,example='SC2032633'),

                                           ):
        # print(new_students_key_info)
        return student_id



