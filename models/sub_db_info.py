from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class SubDbInfo(BaseDBModel):
    """
    """
    __tablename__ = 'lfun_sub_db_info'
    __table_args__ = {'comment': '各学校DB信息表模型'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="班级ID",autoincrement=False)
    db_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库名称",default='')
    db_host: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库地址",default='')
    db_port: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库端口",default='')
    db_user: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库用户",default='')
    db_pwd: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库密码",default='')
    db_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库类型",default='')
    db_status: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库状态",default='')
    db_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库备注",default='')
    db_version: Mapped[str] = mapped_column(String(255),  nullable=True, comment="数据库版本",default='')

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)





