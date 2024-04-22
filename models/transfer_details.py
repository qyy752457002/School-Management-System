from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class TransferDetails(BaseDBModel):

    """
    调动明细表
原单位
原岗位
现单位
现岗位
调动原因
备注
操作人
教师ID
操作时间



    """
    __tablename__ = 'lfun_transfer_details'
    __table_args__ = {'comment': '调动明细表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(nullable=True , comment="教师ID",default=0)  # 与教师表关联，关系为一对n

    old_unit: Mapped[str] = mapped_column(String(255),  nullable=True, comment="原单位",default='')
    old_post: Mapped[str] = mapped_column(String(255),  nullable=True, comment="原岗位",default='')
    new_unit: Mapped[str] = mapped_column(String(255),  nullable=True, comment="现单位",default='')
    new_post: Mapped[str] = mapped_column(String(255),  nullable=True, comment="现岗位",default='')
    transfer_reason: Mapped[str] = mapped_column(String(255),  nullable=True, comment="调动原因",default='')
    transfer_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="备注",default='')
    transfer_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False, comment="操作时间")
    transfer_user: Mapped[str] = mapped_column(String(255),  nullable=True, comment="操作人",default='')
    transfer_user_id: Mapped[int] = mapped_column(  nullable=True , comment="操作人ID",default=0)

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





