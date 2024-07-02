from sqlalchemy import String, Date, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from mini_framework.databases.entities import BaseDBModel
from datetime import date, datetime
from enum import Enum

class BorrowType(str, Enum):
    """
    借动类型
    """
    IN = "borrow_in"
    OUT = "borrow_out"

    @classmethod
    def to_list(cls):
        return [cls.IN, cls.OUT,]


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
    original_unit_id: Mapped[int] = mapped_column(nullable=True, comment="原单位")
    original_unit_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="原单位名称")
    original_position: Mapped[str] = mapped_column(String(64), nullable=True, comment="原岗位")
    original_district_province_id: Mapped[int] = mapped_column(nullable=True, comment="原行政属地省")
    original_district_city_id: Mapped[int] = mapped_column( nullable=True, comment="原行政属地市")
    original_district_area_id: Mapped[int] = mapped_column(nullable=True, comment="原行政属地区")
    original_region_province_id: Mapped[int] = mapped_column( nullable=True, comment="原管辖区域省")
    original_region_city_id: Mapped[int] = mapped_column( nullable=True, comment="原管辖区域市")
    original_region_area_id: Mapped[int] = mapped_column( nullable=True, comment="原管辖区域区")

    borrow_in_date: Mapped[date] = mapped_column(Date, nullable=True, comment="借入日期")
    current_unit_id: Mapped[int] = mapped_column(nullable=True, comment="现单位")
    current_position: Mapped[str] = mapped_column(String(64), nullable=True, comment="现岗位")
    current_unit_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="现单位名称")
    current_district_province_id: Mapped[int] = mapped_column( nullable=True, comment="现行政属地省")
    current_district_city_id: Mapped[int] = mapped_column( nullable=True, comment="现行政属地市")
    current_district_area_id: Mapped[int] = mapped_column(nullable=True, comment="现行政属地区")
    current_region_province_id: Mapped[int] = mapped_column( nullable=True, comment="现管辖区域省")
    current_region_city_id: Mapped[int] = mapped_column( nullable=True, comment="现管辖区域市")
    current_region_area_id: Mapped[int] = mapped_column(nullable=True, comment="现管辖区域区")

    borrow_out_date: Mapped[date] = mapped_column(Date, nullable=True, comment="借出日期")
    borrow_reason: Mapped[str] = mapped_column(String(64), nullable=True, comment="借动原因")
    remark: Mapped[str] = mapped_column(String(64), nullable=True, comment="备注")
    teacher_id: Mapped[int] = mapped_column(nullable=False, comment="教师ID")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
    borrow_type: Mapped[str] = mapped_column(String(255), nullable=False, comment="借动类型")



