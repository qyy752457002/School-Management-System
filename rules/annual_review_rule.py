from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.annual_review_dao import AnnualReviewDAO
from models.annual_review import AnnualReview
from views.models.teacher_extend import AnnualReviewModel,AnnualReviewUpdateModel


@dataclass_inject
class AnnualReviewRule(object):
    annual_review_dao: AnnualReviewDAO

    async def get_annual_review_by_annual_review_id(self, annual_review_id):
        annual_review_db = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewModel)
        return annual_review
    async def add_annual_review(self, annual_review:AnnualReviewModel):
        annual_review_db = view_model_to_orm_model(annual_review, AnnualReview)
        annual_review_db = await self.annual_review_dao.add_annual_review(annual_review_db)
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewModel)
        return annual_review
    async def delete_annual_review(self, annual_review_id):
        exists_annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        if not exists_annual_review:
            raise Exception(f"编号为的{annual_review_id}annual_review不存在")
        annual_review_db = await self.annual_review_dao.delete_annual_review(exists_annual_review)
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewModel, exclude=[""])
        return annual_review
    async def update_annual_review(self, annual_review:AnnualReviewUpdateModel):
        exists_annual_review_info = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review.annual_review_id)
        if not exists_annual_review_info:
            raise Exception(f"编号为{annual_review.annual_review_id}的annual_review不存在")
        need_update_list = []
        for key, value in annual_review.dict().items():
            if value:
                need_update_list.append(key)
        annual_review = await self.annual_review_dao.update_annual_review(annual_review, *need_update_list)
        return annual_review
    async def get_all_annual_review(self, teacher_id):
          annual_review_db = await self.annual_review_dao.get_all_annual_review(teacher_id)
#          annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewModel, exclude=[""])
          annual_review=[]
          for item in annual_review_db:
              annual_review.append(orm_model_to_view_model(item, AnnualReviewModel))
          return annual_review_db
