from mini_framework.web.views import BaseView
from mini_framework.design_patterns.depend_inject import get_injector
from mini_framework.web.views import BaseView
from fastapi import Query

from views.models.teacher_extend import TeacherLearnExperienceModel, TeacherLearnExperienceUpdateModel
from rules.teacher_learn_experience_rule import TeacherLearnExperienceRule

class TeacherLearnExperienceView(BaseView):
    def __init__(self):
       super().__init__()

       self.teacher_learn_experience_rule = get_injector(TeacherLearnExperienceRule)

    async def get_teacher_learn_experience(self,
                  teacher_learn_experience_id: int= Query(None, title="teacher_learn_experienceID", description="teacher_learn_experienceID", example=1234)
                  ):
        res =await self.teacher_learn_experience_rule.get_teacher_learn_experience_by_teacher_learn_experience_id(teacher_learn_experience_id)
        return res

    async def post_teacher_learn_experience(self, teacher_learn_experience:TeacherLearnExperienceModel):
        res = await self.teacher_learn_experience_rule.add_teacher_learn_experience(teacher_learn_experience)
        return res

    async def delete_teacher_learn_experience(self,
                  teacher_learn_experience_id: int= Query(None, title="teacher_learn_experienceID", description="teacher_learn_experienceID", example=1234)
                  ):
        await self.teacher_learn_experience_rule.delete_teacher_learn_experience(teacher_learn_experience_id)
    async def put_teacher_learn_experience(self, teacher_learn_experience:TeacherLearnExperienceUpdateModel):
        res = await self.teacher_learn_experience_rule.update_teacher_learn_experience(teacher_learn_experience)
        return res

    async def get_teacher_learn_experience_all(self,teacher_id: int= Query(None, title="teacher_learn_experienceID", description="teacher_learn_experienceID", example=1234)):
        return await self.teacher_learn_experience_rule.get_all_teacher_learn_experience(teacher_id)

