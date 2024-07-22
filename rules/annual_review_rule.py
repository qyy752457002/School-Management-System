from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model
from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.web.std_models.page import PaginatedResponse, PageRequest
from daos.annual_review_dao import AnnualReviewDAO
from models.annual_review import AnnualReview
from views.models.teacher_extend import AnnualReviewModel, AnnualReviewUpdateModel
from daos.teachers_dao import TeachersDao
from business_exceptions.teacher import TeacherNotFoundError,AnnualReviewNotFoundError
from mini_framework.utils.snowflake import SnowflakeIdGenerator


@dataclass_inject
class AnnualReviewRule(object):
    annual_review_dao: AnnualReviewDAO
    teachers_dao: TeachersDao

    async def get_annual_review_by_annual_review_id(self, annual_review_id):
        annual_review_db = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewUpdateModel)
        return annual_review

    async def add_annual_review(self, annual_review: AnnualReviewModel):
        exits_teacher = await self.teachers_dao.get_teachers_by_id(annual_review.teacher_id)
        if not exits_teacher:
            raise TeacherNotFoundError()
        annual_review_db = view_model_to_orm_model(annual_review, AnnualReview)
        annual_review_db.annual_review_id = SnowflakeIdGenerator(1, 1).generate_id()
        annual_review_db = await self.annual_review_dao.add_annual_review(annual_review_db)
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewUpdateModel)
        return annual_review

    async def delete_annual_review(self, annual_review_id):
        exists_annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        if not exists_annual_review:
            raise AnnualReviewNotFoundError()
        annual_review_db = await self.annual_review_dao.delete_annual_review(exists_annual_review)
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewUpdateModel, exclude=[""])
        return annual_review

    async def update_annual_review(self, annual_review: AnnualReviewUpdateModel):
        exists_annual_review_info = await self.annual_review_dao.get_annual_review_by_annual_review_id(
            annual_review.annual_review_id)
        if not exists_annual_review_info:
            raise AnnualReviewNotFoundError()
        need_update_list = []
        for key, value in annual_review.dict().items():
            if value:
                need_update_list.append(key)
        annual_review = await self.annual_review_dao.update_annual_review(annual_review, *need_update_list)
        return annual_review

    async def get_all_annual_review(self, teacher_id):
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        if not exit_teacher:
            raise TeacherNotFoundError()
        annual_review_db = await self.annual_review_dao.get_all_annual_review(teacher_id)
        annual_review = []
        for item in annual_review_db:
            annual_review.append(orm_model_to_view_model(item, AnnualReviewUpdateModel))
        return annual_review_db


    async def submitting(self,annual_review_id):
        annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        if not annual_review:
            raise AnnualReviewNotFoundError()
        annual_review.approval_status = "submitting"
        return await self.annual_review_dao.update_annual_review(annual_review, "approval_status")

    async def submitted(self,annual_review_id):
        annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        if not annual_review:
            raise AnnualReviewNotFoundError()
        annual_review.approval_status = "submitted"
        return await self.annual_review_dao.update_annual_review(annual_review, "approval_status")

    async def approved(self,annual_review_id):
        annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        if not annual_review:
            raise AnnualReviewNotFoundError()
        annual_review.approval_status = "approved"
        return await self.annual_review_dao.update_annual_review(annual_review, "approval_status")

    async def rejected(self,annual_review_id):
        annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        if not annual_review:
            raise AnnualReviewNotFoundError()
        annual_review.approval_status = "rejected"
        return await self.annual_review_dao.update_annual_review(annual_review, "approval_status")

