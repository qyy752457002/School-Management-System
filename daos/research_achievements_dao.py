from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import select, func, update
from mini_framework.databases.entities.dao_base import DAOBase, get_update_contents
from mini_framework.databases.queries.pages import Paging
from mini_framework.web.std_models.page import PageRequest

from models.research_achievements import ResearchAchievements
from views.models.teacher_extend import ResearchAchievementsQueryModel
from models.teachers import Teacher


class ResearchAchievementsDAO(DAOBase):

    async def add_research_achievements(self, research_achievements: ResearchAchievements):
        session = await self.master_db()
        session.add(research_achievements)
        await session.commit()
        await session.refresh(research_achievements)
        return research_achievements

    async def get_research_achievements_count(self):
        session = await self.slave_db()
        result = await session.execute(select(func.count()).select_from(ResearchAchievements))
        return result.scalar()

    async def delete_research_achievements(self, research_achievements: ResearchAchievements):
        session = await self.master_db()
        return await self.delete(session, research_achievements)

    async def get_research_achievements_by_research_achievements_id(self, research_achievements_id):
        session = await self.slave_db()
        result = await session.execute(select(ResearchAchievements).where(
            ResearchAchievements.research_achievements_id == research_achievements_id,
            ResearchAchievements.is_deleted == False))
        return result.scalar_one_or_none()

    async def query_research_achievements_with_page(self, pageQueryModel, page_request: PageRequest):
        query = select(ResearchAchievements)
        paging = await self.query_page(query, page_request)
        return paging

    async def update_research_achievements(self, research_achievements, *args, is_commit=True):
        session = await self.master_db()
        update_contents = get_update_contents(research_achievements, *args)
        query = update(ResearchAchievements).where(
            ResearchAchievements.research_achievements_id == research_achievements.research_achievements_id).values(
            **update_contents)
        return await self.update(session, query, research_achievements, update_contents, is_commit=is_commit)

    async def get_all_research_achievements(self, teacher_id):
        session = await self.slave_db()
        query = select(ResearchAchievements.research_achievements_id, ResearchAchievements.teacher_id,
                       ResearchAchievements.research_achievement_type,
                       ResearchAchievements.type,
                       ResearchAchievements.representative_or_project, ResearchAchievements.name,
                       ResearchAchievements.disciplinary_field, ResearchAchievements.role).join(Teacher,
                                                                                                ResearchAchievements.teacher_id == Teacher.teacher_id).where(
            ResearchAchievements.teacher_id == teacher_id, ResearchAchievements.is_deleted == False)

        result = await session.execute(query)
        column_names = query.columns.keys()

        result = result.fetchall()
        items = []
        for item in result:
            if issubclass(item[0].__class__, BaseDBModel):
                items.append(item[0])
            else:
                item_dict = dict(zip(column_names, item))
                items.append(item_dict)
        return items
