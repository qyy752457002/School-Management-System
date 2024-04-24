from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.research_achievements_dao import ResearchAchievementsDAO
from models.research_achievements import ResearchAchievements
from views.models.teacher_extend import ResearchAchievementsModel, ResearchAchievementsUpdateModel, ResearchAchievementsQueryModel,ResearchAchievementsQueryReModel


@dataclass_inject
class ResearchAchievementsRule(object):
    research_achievements_dao: ResearchAchievementsDAO

    async def get_research_achievements_by_research_achievements_id(self, research_achievements_id):
        research_achievements_db = await self.research_achievements_dao.get_research_achievements_by_research_achievements_id(
            research_achievements_id)
        research_achievements = orm_model_to_view_model(research_achievements_db, ResearchAchievementsModel)
        return research_achievements

    async def add_research_achievements(self, research_achievements: ResearchAchievementsModel):
        research_achievements_db = view_model_to_orm_model(research_achievements, ResearchAchievements)
        research_achievements_db = await self.research_achievements_dao.add_research_achievements(
            research_achievements_db)
        research_achievements = orm_model_to_view_model(research_achievements_db, ResearchAchievementsModel)
        return research_achievements

    async def delete_research_achievements(self, research_achievements_id):
        exists_research_achievements = await self.research_achievements_dao.get_research_achievements_by_research_achievements_id(
            research_achievements_id)
        if not exists_research_achievements:
            raise Exception(f"编号为的{research_achievements_id}research_achievements不存在")
        research_achievements_db = await self.research_achievements_dao.delete_research_achievements(
            exists_research_achievements)
        research_achievements = orm_model_to_view_model(research_achievements_db, ResearchAchievementsModel,
                                                        exclude=[""])
        return research_achievements

    async def update_research_achievements(self, research_achievements: ResearchAchievementsUpdateModel):
        exists_research_achievements_info = await self.research_achievements_dao.get_research_achievements_by_research_achievements_id(
            research_achievements.research_achievements_id)
        if not exists_research_achievements_info:
            raise Exception(f"编号为{research_achievements.research_achievements_id}的research_achievements不存在")
        need_update_list = []
        for key, value in research_achievements.dict().items():
            if value:
                need_update_list.append(key)
        research_achievements = await self.research_achievements_dao.update_research_achievements(research_achievements,
                                                                                                  *need_update_list)
        return research_achievements

    async def get_all_research_achievements(self, teacher_id):
        research_achievements_db = await self.research_achievements_dao.get_all_research_achievements(teacher_id)
        #          research_achievements = orm_model_to_view_model(research_achievements_db, ResearchAchievementsModel, exclude=[""])
        research_achievements = []
        for item in research_achievements_db:
            research_achievements.append(orm_model_to_view_model(item, ResearchAchievementsModel))
        return research_achievements_db

    async def query_research_achievements_with_page(self, query_model: ResearchAchievementsQueryModel, page_request: PageRequest):
        paging = await self.research_achievements_dao.query_research_achievements_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, ResearchAchievementsQueryReModel)
        return paging_result
