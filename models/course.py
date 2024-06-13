from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class Course(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_course'
    __table_args__ = {'comment': '学科表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)
    school_type: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="教育阶段/学校类别 例如 小学 初中 多个逗号隔开")
    city: Mapped[str] = mapped_column(String(64), nullable=True,default='', comment="城市")

    district: Mapped[str] = mapped_column(String(64), nullable=True, comment="",default='')
    school_id: Mapped[int] = mapped_column( comment="学校ID",nullable=True,default=0)
    course_no: Mapped[str] = mapped_column(String(24), nullable=True,default='', comment="学科编码")
    grade_id: Mapped[int] = mapped_column( comment="年级ID",nullable=True,default=0)
    course_name: Mapped[str] = mapped_column(String(24), nullable=False, comment="学科名称")

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

    # @staticmethod
    # def seed():
    #     return [
    #         Course(id=149,school_id=0,
    #                course_no="11",grade_id=0,
    #                course_name="品德与生活(社会)",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学'),
    #
    #         Course(id=1,school_id=0,
    #                course_no="14",grade_id=0,
    #                course_name="数学",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course(id=2,school_id=0,
    #                course_no="13",grade_id=0,
    #                course_name="语文",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course(id=5,school_id=0,
    #                course_no="15",grade_id=0,
    #                course_name="科学",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中'),
    #
    #         Course(id=150,school_id=0,
    #                course_no="12",grade_id=0,
    #                course_name="思想品德(政治)",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='初中,普通高中'),
    #         Course(id=151,school_id=0,
    #                course_no="16",grade_id=0,
    #                course_name="物理",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='初中,普通高中'),
    #         Course(id=152,school_id=0,
    #                course_no="17",grade_id=0,
    #                course_name="化学",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='初中,普通高中'),
    #         Course(id=153,school_id=0,
    #                course_no="18",grade_id=0,
    #                course_name="生物",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='初中,普通高中'),
    #         Course(id=154,school_id=0,
    #                course_no="19",grade_id=0,
    #                course_name="历史与社会",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='初中'),
    #         Course(id=155,school_id=0,
    #                course_no="20",grade_id=0,
    #                course_name="地理",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='初中,普通高中'),
    #         Course(id=156,school_id=0,
    #                course_no="21",grade_id=0,
    #                course_name="历史",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='初中,普通高中'),
    #         Course(id=157,school_id=0,
    #                course_no="23",grade_id=0,
    #                course_name="艺术",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course(id=158,school_id=0,
    #                course_no="22",grade_id=0,
    #                course_name="体育与健康",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,
    #                course_no="24",grade_id=0,
    #                course_name="音乐",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,
    #                 course_no="25",grade_id=0,
    #                 course_name="美术",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,
    #                 course_no="26",grade_id=0,
    #                 course_name="信息技术",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='普通高中'),
    #         Course( school_id=0,
    #                 course_no="27",grade_id=0,
    #                 course_name="通用技术",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='普通高中'),
    #         Course( school_id=0,course_no="40",grade_id=0,  course_name="外语",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,course_no="41",grade_id=0,  course_name="英语",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,course_no="42",grade_id=0,  course_name="日语",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,course_no="43",grade_id=0,  course_name="俄语",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,course_no="49",grade_id=0,  course_name="其他外国语",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,course_no="60",grade_id=0,  course_name="综合实践活动",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中,普通高中'),
    #         Course( school_id=0,course_no="62",grade_id=0,  course_name="劳动与技术",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中'),
    #         Course( school_id=0,course_no="61",grade_id=0,  course_name="信息技术",created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False,district='',school_type='小学,初中'),
    #     ]



