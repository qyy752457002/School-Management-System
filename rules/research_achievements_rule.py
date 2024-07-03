from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.research_achievements_dao import ResearchAchievementsDAO
from models.research_achievements import ResearchAchievements
from views.models.teacher_extend import ResearchAchievementsModel, ResearchAchievementsUpdateModel, \
    ResearchAchievementsQueryModel, ResearchAchievementsQueryReModel
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError, ResearchAchievementsNotFoundError
from mini_framework.utils.snowflake import SnowflakeIdGenerator


@dataclass_inject
class ResearchAchievementsRule(object):
    research_achievements_dao: ResearchAchievementsDAO
    teachers_dao: TeachersDao

    async def get_research_achievements_by_research_achievements_id(self, research_achievements_id):
        research_achievements_db = await self.research_achievements_dao.get_research_achievements_by_research_achievements_id(
            research_achievements_id)
        research_achievements = orm_model_to_view_model(research_achievements_db, ResearchAchievementsModel)
        return research_achievements

    async def add_research_achievements(self, research_achievements: ResearchAchievementsModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(research_achievements.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        research_achievements_db = view_model_to_orm_model(research_achievements, ResearchAchievements)
        research_achievements_db.research_achievements_id = SnowflakeIdGenerator(1, 1).generate_id()
        research_achievements_db = await self.research_achievements_dao.add_research_achievements(
            research_achievements_db)
        research_achievements = orm_model_to_view_model(research_achievements_db, ResearchAchievementsModel)
        return research_achievements

    async def delete_research_achievements(self, research_achievements_id):
        exists_research_achievements = await self.research_achievements_dao.get_research_achievements_by_research_achievements_id(
            research_achievements_id)
        if not exists_research_achievements:
            raise ResearchAchievementsNotFoundError()
        research_achievements_db = await self.research_achievements_dao.delete_research_achievements(
            exists_research_achievements)
        research_achievements = orm_model_to_view_model(research_achievements_db, ResearchAchievementsModel,
                                                        exclude=[""])
        return research_achievements

    async def update_research_achievements(self, research_achievements: ResearchAchievementsUpdateModel):
        exists_research_achievements_info = await self.research_achievements_dao.get_research_achievements_by_research_achievements_id(
            research_achievements.research_achievements_id)
        if not exists_research_achievements_info:
            raise ResearchAchievementsNotFoundError()
        need_update_list = []
        for key, value in research_achievements.dict().items():
            if value:
                need_update_list.append(key)
        research_achievements = await self.research_achievements_dao.update_research_achievements(research_achievements,
                                                                                                  *need_update_list)
        return research_achievements

    async def get_all_research_achievements(self, teacher_id):
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        research_achievements_db = await self.research_achievements_dao.get_all_research_achievements(teacher_id)
        research_achievements = []
        for item in research_achievements_db:
            research_achievements.append(orm_model_to_view_model(item, ResearchAchievementsQueryReModel))
        return research_achievements

    async def query_research_achievements_with_page(self, query_model: ResearchAchievementsQueryModel,
                                                    page_request: PageRequest):
        paging = await self.research_achievements_dao.query_research_achievements_with_page(query_model, page_request)
        paging_result = PaginatedResponse.from_paging(paging, ResearchAchievementsQueryReModel)
        return paging_result
