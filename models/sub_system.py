from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class SubSystem(BaseDBModel):
    """
    system_name: str = Field(..., title="",description="系统名称",examples=['学校版'])
    system_no: str = Field(..., title="系统编号", description="系统编号",examples=['02'])
    system_url: str = Field(..., title="", description="系统url",examples=['www.fsdfsd.cc'])
    system_icon: str = Field(..., title="", description="系统icon",examples=['www.dd.cc/343.jpg'])
    system_description: str = Field(..., title="", description="系统简述",examples=['学校版的教育登录'])
    """
    __tablename__ = 'lfun_sub_system'
    __table_args__ = {'comment': '子系统表模型'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="班级ID",autoincrement=False)
    system_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="系统名称",default='')
    system_no: Mapped[str] = mapped_column(String(255),  nullable=True, comment="系统编号",default='')
    system_url: Mapped[str] = mapped_column(String(255),  nullable=True, comment="系统url",default='')
    system_icon: Mapped[str] = mapped_column(String(255),  nullable=True, comment="系统icon",default='')
    system_description: Mapped[str] = mapped_column(String(255),  nullable=True, comment="系统简述",default='')
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





