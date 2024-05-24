from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date

class TeacherBorrow(BaseDBModel):
    """
    teacher_borrow：teacher_borrow_id
    原单位：original_unit
    原岗位：original_position
    原行政属地：original_district
    现单位：current_unit
    现岗位：current_position
    现行政属地：current_district
    借动类型：borrow_type
    借动原因：borrow_reason
    备注：remark
    操作人：operator
    教师ID：teacher_id
    操作时间：operation_time
    删除状态：is_deleted
    """
    __tablename__ = 'lfun_teacher_borrow'
    __table_args__ = {'comment': 'teacher_borrow信息表'}

    teacher_borrow_id: Mapped[int] = mapped_column(primary_key=True, comment="teacher_borrowID")
    original_unit: Mapped[str] = mapped_column(String(64), nullable=False, comment="原单位")
    original_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="原岗位")
    original_district: Mapped[str] = mapped_column(String(64), nullable=False, comment="原行政属地")
    current_unit: Mapped[str] = mapped_column(String(64), nullable=False, comment="现单位")
    current_position: Mapped[str] = mapped_column(String(64), nullable=False, comment="现岗位")
    current_district: Mapped[str] = mapped_column(String(64), nullable=False, comment="现行政属地")
    borrow_type: Mapped[str] = mapped_column(String(64), nullable=False, comment="借动类型")
    borrow_reason: Mapped[str] = mapped_column(String(64), nullable=False, comment="借动原因")
    remark: Mapped[str] = mapped_column(String(64), nullable=False, comment="备注")
    operator: Mapped[str] = mapped_column(String(64), nullable=False, comment="操作人")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    operation_time: Mapped[date] = mapped_column(Date, nullable=False, comment="操作时间")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    
