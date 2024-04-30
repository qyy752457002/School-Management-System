from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class AttachRelations(BaseDBModel):

    """
    附件关系表
  附件ID attach_id
  附件关联的主体  ID
  attach_owner_id 附件主体
   attach_owner 枚举: 例如 planning_school / school / student/teacher 等



    """
    __tablename__ = 'lfun_attach_relations'
    __table_args__ = {'comment': '附件关系表表模型'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    attach_owner_id: Mapped[int] = mapped_column(  nullable=True , comment="附件主体ID",default=0)
    attach_owner: Mapped[str] = mapped_column(String(255),  nullable=True, comment="附件主体",default='')
    attach_id: Mapped[int] = mapped_column(  nullable=True , comment="附件ID",default=0)
    attach_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="附件类型",default='')
    attach_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="附件备注",default='')

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)







