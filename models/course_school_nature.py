from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class CourseSchoolNature(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_course_school_nature'
    __table_args__ = {'comment': '课程和学校关系表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)
    course_no: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码")
    school_nature: Mapped[str] = mapped_column(String(40), nullable=True,default='', comment="学校性质 2级或者3级")
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

    # @staticmethod
    # def seed():
    #     return [
    #         CourseSchoolNature(
    #             course_no='12',
    #             school_nature='303',
    #             created_uid=0,
    #             updated_uid=0,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #             is_deleted=False,
    #         ),
    #         CourseSchoolNature(
    #             course_no='13',
    #             school_nature='小学',
    #             created_uid=0,
    #             updated_uid=0,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #             is_deleted=False,
    #         ),
    #         CourseSchoolNature(
    #             course_no='13',
    #             school_nature='初中',
    #             created_uid=0,
    #             updated_uid=0,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #             is_deleted=False,
    #         ),
    #         CourseSchoolNature(
    #             course_no='13',
    #             school_nature='普通高中',
    #             created_uid=0,
    #             updated_uid=0,
    #             created_at=datetime.now(),
    #             updated_at=datetime.now(),
    #             is_deleted=False,
    #         ),
    #     ]



