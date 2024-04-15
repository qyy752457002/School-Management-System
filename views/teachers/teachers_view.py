from mini_framework.web.views import BaseView

from views.models.teachers import Teachers
# from fastapi import Field
from fastapi import Query


class TeachersView(BaseView):
    async def get(self,
                  teacher_name: str = Query(None, title="教师名称", description="教师名称", min_length=1, max_length=20,
                                            example='张三'),
                  teacher_id_number: str = Query(None, description="证件号", min_length=1, max_length=20,
                                                 example='123456789012345678'),
                  ):
        res = Teachers(
            teacher_name=teacher_name,
            teacher_id_number=teacher_id_number,
            teacher_gender="男",
            teacher_id_type="身份证",
            teacher_date_of_birth="1990-01-01",
            teacher_employer="xx学校",
            teacher_avatar="http://www.baidu.com",
            teacher_approval_status="通过"

        )
        return res

    async def post(self, teachers: Teachers):
        print(teachers)
        return teachers
