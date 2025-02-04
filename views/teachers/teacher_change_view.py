from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query

from views.models.teacher_change import TeacherChangeLogModel
from rules.teacher_change_rule import TeacherChangeRule

class TeacherChangeView(BaseView):
    def __init__(self):
        super().__init__()
        self.teacher_change_rule = get_injector(TeacherChangeRule)

    async def get_all_teacher_change_detail(self,
                                            teacher_id: int = Query(None, title="teacher_changeID",
                                                                    description="teacher_changeID", example=1234),
                                            teacher_change_id: int = Query(None, title="teacher_changeID",
                                                                           description="teacher_changeID",
                                                                           example=1234)):
        res = await self.teacher_change_rule.get_teacher_change_detail_by_teacher_id(teacher_id, teacher_change_id)
        return res

    async def post_teacher_change(self, teacher_change: TeacherChangeLogModel):
        res = await self.teacher_change_rule.add_teacher_change(teacher_change)
        return res

    # async def post_teacher_change_detail(self, teacher_change_detail: TeacherChangeDetail):
    #     res = await self.teacher_change_rule.add_teacher_change_detail(teacher_change_detail)
    #     return res

    async def get_teacher_change_all(self, teacher_id: int = Query(None, title="teacher_changeID",
                                                                   description="teacher_changeID", example=1234)):
        return await self.teacher_change_rule.get_all_teacher_change(teacher_id)
