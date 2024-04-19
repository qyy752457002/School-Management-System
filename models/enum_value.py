from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class EnumValue(BaseDBModel):
    """
    enum_name : str = Field(..., title="",description="枚举类型的名称",examples=['国家'])
    enum_value : str = Field(..., title="", description="枚举的具体值",examples=['韩国','中国'])
    description : str = Field(..., title="", description="枚举值的描述或标签",examples=[''])
    sort_number: int = Field(..., title="", description="排序序号",examples=[ 2])
    parent_id: str = Field(None, title="", description="父级ID",examples=[''])
    """
    __tablename__ = 'lfun_enum_value'
    __table_args__ = {'comment': '枚举表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="ID",autoincrement=True)
    enum_name: Mapped[str] = mapped_column(String(60), nullable=True,default='', comment="枚举类型的名称")
    enum_value: Mapped[str] = mapped_column(String(60), nullable=True,default='', comment="枚举的具体值")
    description: Mapped[str] = mapped_column(String(60), nullable=True,default='', comment="枚举值的描述或标签")
    sort_number: Mapped[int] = mapped_column(nullable=True,default=0, comment="排序序号")
    parent_id: Mapped[str] = mapped_column(String(60), nullable=True,default='', comment="父级ID")
    is_enabled: Mapped[bool] = mapped_column( nullable=False , comment="是否启用",default=True)
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)







