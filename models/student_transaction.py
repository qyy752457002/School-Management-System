from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class StudentTransaction(BaseDBModel):
    """
    转学休学入学毕业申请表
    province_id: str = Query(...,   description="省份",min_length=1,max_length=20,examples=["1"]),
    city_id: str = Query(...,   description="市",min_length=1,max_length=20,examples=["1"]),
    area_id: str = Query(...,   description="区",min_length=1,max_length=20,examples=["1"]),
    district_id: str = Query(...,   description="区县",min_length=1,max_length=20,examples=["1"]),
    transfer_in_type: str = Query(...,   description="转入类型",min_length=1,max_length=20,examples=["指定日期转入"]),
    school_name: str = Query(..., title="", description="学校名称",examples=["XXxiaoxue"])
    出入方向
    session: str = Query(..., title="", description="届别",examples=["2003"])
    attached_class: str = Query(..., title="", description="附设班",examples=["3班"])
    grade_id: str = Query(..., title="", description="年级ID",examples=["1"])
    class_id: str = Query(..., title="", description="班级id",examples=["125"])
    major_id: str = Query(..., title="", description="专业",examples=["农业"])
    专业
    """
    __tablename__ = 'lfun_student_transaction'
    __table_args__ = {'comment': '转学休学入学毕业申请表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID", autoincrement=True)
    student_id: Mapped[int] = mapped_column(nullable=True, comment="学生ID", default=0)
    student_no: Mapped[str] = mapped_column(String(255), nullable=True, comment="学籍号", default='')
    student_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="学生姓名", default='')
    current_org: Mapped[str] = mapped_column(String(255), nullable=True, comment="当前机构", default='')
    apply_user: Mapped[str] = mapped_column(String(255), nullable=True, comment="申请人", default='')
    apply_time: Mapped[str] = mapped_column(String(255), nullable=True, comment="申请时间", default='')
    out_school_id: Mapped[int] = mapped_column(nullable=True, comment="转出学校ID", default=0)
    in_school_id: Mapped[int] = mapped_column(nullable=True, comment="转入学校ID", default=0)
    in_grade: Mapped[str] = mapped_column(String(255), nullable=True, comment="转入年级", default='')
    in_class: Mapped[str] = mapped_column(String(255), nullable=True, comment="装入班级", default='')
    in_date: Mapped[str] = mapped_column(String(255), nullable=True, comment="装入日期", default='')
    out_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="转出类型", default='')
    out_grade: Mapped[str] = mapped_column(String(255), nullable=True, comment="转出年级", default='')
    out_class: Mapped[str] = mapped_column(String(255), nullable=True, comment="装出班级", default='')
    country_no: Mapped[str] = mapped_column(String(255), nullable=True, comment="国家学籍号码", default='')
    out_date: Mapped[str] = mapped_column(String(255), nullable=True, comment="转出日期", default='')
    reason: Mapped[str] = mapped_column(String(255), nullable=True, comment="转学原因", default='')
    is_valid: Mapped[bool] = mapped_column(nullable=False, comment="是否有效", default=True)

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False,
                               comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
