from mini_framework.web.views import BaseView

from views.models.students import NewStudents, NewStudentsQuery, StudentsKeyinfo, StudentsBaseInfo
# from fastapi import Field
from fastapi import Query, Depends
from pydantic import BaseModel, Field
from mini_framework.web.std_models.page import PageRequest
from mini_framework.web.std_models.page import PaginatedResponse
from datetime import date


class CurrentStudentsView(BaseView):
    # 在校生流出
    async def patch_flowout(self,    student_id: str = Query(...,   description="学生id",min_length=1,max_length=20,example='SC2032633'),
                            flowout_time    :str= Query(..., description="流出时间" ,min_length=1,max_length=20,example='2020-10-10'),
                            flowout_reason   :str= Query(..., description="流出原因" ,min_length=1,max_length=20,example='家庭搬迁'),
                            ):
        # print(new_students_key_info)
        return student_id



