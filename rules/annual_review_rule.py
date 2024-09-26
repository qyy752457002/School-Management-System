from mini_framework.design_patterns.depend_inject import dataclass_inject
from mini_framework.utils.snowflake import SnowflakeIdGenerator
from mini_framework.web.toolkit.model_utilities import orm_model_to_view_model, view_model_to_orm_model

from business_exceptions.teacher import TeacherNotFoundError, AnnualReviewNotFoundError
from daos.annual_review_dao import AnnualReviewDAO
from daos.teachers_dao import TeachersDao
from models.annual_review import AnnualReview
from views.models.teacher_extend import AnnualReviewModel, AnnualReviewUpdateModel


@dataclass_inject
class AnnualReviewRule(object):
    # 注入AnnualReviewDAO和TeachersDao
    annual_review_dao: AnnualReviewDAO
    teachers_dao: TeachersDao

    # 根据annual_review_id获取AnnualReview
    async def get_annual_review_by_annual_review_id(self, annual_review_id):
        # 从数据库中获取AnnualReview
        annual_review_db = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        # 将数据库中的AnnualReview转换为视图模型
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewUpdateModel)
        return annual_review

    # 添加AnnualReview
    async def add_annual_review(self, annual_review: AnnualReviewModel):
        # 根据teacher_id获取教师信息
        exits_teacher = await self.teachers_dao.get_teachers_by_id(annual_review.teacher_id)
        # 如果教师不存在，抛出TeacherNotFoundError异常
        if not exits_teacher:
            raise TeacherNotFoundError()
        # 将视图模型转换为数据库模型
        annual_review_db = view_model_to_orm_model(annual_review, AnnualReview)
        # 生成annual_review_id
        annual_review_db.annual_review_id = SnowflakeIdGenerator(1, 1).generate_id()
        # 将AnnualReview添加到数据库中
        annual_review_db = await self.annual_review_dao.add_annual_review(annual_review_db)
        # 将数据库中的AnnualReview转换为视图模型
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewUpdateModel)
        return annual_review

    # 根据年审ID删除年审
    async def delete_annual_review(self, annual_review_id):
        # 根据年审ID查询年审信息
        exists_annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        # 如果年审信息不存在，抛出年审未找到异常
        if not exists_annual_review:
            raise AnnualReviewNotFoundError()
        # 根据年审信息删除年审
        annual_review_db = await self.annual_review_dao.delete_annual_review(exists_annual_review)
        # 将年审数据库模型转换为视图模型
        annual_review = orm_model_to_view_model(annual_review_db, AnnualReviewUpdateModel, exclude=[""])
        # 返回年审信息
        return annual_review

    # 更新年审
    async def update_annual_review(self, annual_review: AnnualReviewUpdateModel):
        # 根据年审ID查询年审信息
        exists_annual_review_info = await self.annual_review_dao.get_annual_review_by_annual_review_id(
            annual_review.annual_review_id)
        # 如果年审信息不存在，抛出年审未找到异常
        if not exists_annual_review_info:
            raise AnnualReviewNotFoundError()
        # 需要更新的字段列表
        need_update_list = []
        # 遍历年审信息，将需要更新的字段添加到列表中
        for key, value in annual_review.dict().items():
            if value:
                need_update_list.append(key)
        # 更新年审信息
        annual_review = await self.annual_review_dao.update_annual_review(annual_review, *need_update_list)
        # 返回年审信息
        return annual_review

    # 获取所有年审
    async def get_all_annual_review(self, teacher_id):
        # 根据教师ID查询教师信息
        exit_teacher = await self.teachers_dao.get_teachers_by_id(teacher_id)
        # 如果教师信息不存在，抛出教师未找到异常
        if not exit_teacher:
            raise TeacherNotFoundError()
        # 根据教师ID查询所有年审信息
        annual_review_db = await self.annual_review_dao.get_all_annual_review(teacher_id)
        # 将年审数据库模型转换为视图模型
        annual_review = []
        for item in annual_review_db:
            annual_review.append(orm_model_to_view_model(item, AnnualReviewUpdateModel))
        # 返回年审信息
        return annual_review_db

    # 提交年审
    async def submitting(self, annual_review_id):
        # 根据年审ID查询年审信息
        annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        # 如果年审信息不存在，抛出年审未找到异常
        if not annual_review:
            raise AnnualReviewNotFoundError()
        # 将年审状态设置为提交中
        annual_review.approval_status = "submitting"
        # 更新年审信息
        return await self.annual_review_dao.update_annual_review(annual_review, "approval_status")

    # 已提交年审
    async def submitted(self, annual_review_id):
        # 根据年审ID查询年审信息
        annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        # 如果年审信息不存在，抛出年审未找到异常
        if not annual_review:
            raise AnnualReviewNotFoundError()
        # 将年审状态设置为已提交
        annual_review.approval_status = "submitted"
        # 更新年审信息
        return await self.annual_review_dao.update_annual_review(annual_review, "approval_status")

    # 已批准年审
    async def approved(self, annual_review_id):
        # 根据年审ID查询年审信息
        annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        # 如果年审信息不存在，抛出年审未找到异常
        if not annual_review:
            raise AnnualReviewNotFoundError()
        # 将年审状态设置为已批准
        annual_review.approval_status = "approved"
        # 更新年审信息
        return await self.annual_review_dao.update_annual_review(annual_review, "approval_status")

    # 已拒绝年审
    async def rejected(self, annual_review_id):
        # 根据年审ID查询年审信息
        annual_review = await self.annual_review_dao.get_annual_review_by_annual_review_id(annual_review_id)
        # 如果年审信息不存在，抛出年审未找到异常
        if not annual_review:
            raise AnnualReviewNotFoundError()
        # 将年审状态设置为已拒绝
        annual_review.approval_status = "rejected"
        # 更新年审信息
        return await self.annual_review_dao.update_annual_review(annual_review, "approval_status")
