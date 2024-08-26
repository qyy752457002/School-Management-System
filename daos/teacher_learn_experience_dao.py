from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.teacher_learn_experience import TeacherLearnExperience
from models.teachers import Teacher


class TeacherLearnExperienceDAO(DAOBase):

    async def add_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperience):
        session = await self.master_db()
        session.add(teacher_learn_experience)
        await session.commit()
        await session.refresh(teacher_learn_experience)
        return teacher_learn_experience

    async def get_teacher_learn_experience_count(self, ):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(TeacherLearnExperience))
        return result.scalar()

    async def delete_teacher_learn_experience(self, teacher_learn_experience: TeacherLearnExperience):
        session = await self.master_db()
        return await self.delete(session, teacher_learn_experience)


    async def get_teacher_learn_experience_by_teacher_learn_experience_id(self, teacher_learn_experience_id):
        session = await self.slave_db()
        result = await session.execute(select(TeacherLearnExperience).where(
            TeacherLearnExperience.teacher_learn_experience_id == teacher_learn_experience_id,TeacherLearnExperience.is_deleted == False))
        return result.scalar_one_or_none()



    async def update_teacher_learn_experience(self, teacher_learn_experience, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(teacher_learn_experience, *args)
        query = update(TeacherLearnExperience).where(
            TeacherLearnExperience.teacher_learn_experience_id == teacher_learn_experience.teacher_learn_experience_id).values(
            **update_contents)
        return await self.update(session, query, teacher_learn_experience, update_contents, is_commit=is_commit)

    ##查询有问题
    async def get_all_teacher_learn_experience(self, teacher_id):
        session = await self.slave_db()
        query = select(TeacherLearnExperience).join(Teacher,
                                                    TeacherLearnExperience.teacher_id == Teacher.teacher_id).where(
            TeacherLearnExperience.teacher_id == teacher_id,TeacherLearnExperience.is_deleted == False)
        result = await session.execute(query)
        return result.scalars().all()
