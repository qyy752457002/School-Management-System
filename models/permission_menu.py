from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class PermissionMenu(BaseDBModel):

    """
    菜单权限表
    权限id
    父级菜单id

    """
    __tablename__ = 'lfun_permission_menu'
    __table_args__ = {'comment': '菜单权限表'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="班级ID",autoincrement=False)
    menu_name: Mapped[str] = mapped_column(String(64),  nullable=True, comment="菜单名称",default='')
    menu_path: Mapped[str] = mapped_column(String(64),  nullable=True, comment="菜单路径",default='')
    resource_code: Mapped[str] = mapped_column(String(128),  nullable=True, comment="资源编码-用于资源和菜单的绑定",default='')
    action: Mapped[str] = mapped_column(String(600),  nullable=True, comment="允许的资源动作",default='')
    menu_icon: Mapped[str] = mapped_column(String(255),  nullable=True, comment="菜单图标",default='')
    menu_type: Mapped[str] = mapped_column(String(255),  nullable=True, comment="菜单类型",default='')
    menu_code: Mapped[str] = mapped_column(String(255),  nullable=True, comment="菜单简码",default='')
    menu_status: Mapped[str] = mapped_column(String(255),  nullable=True, comment="菜单状态",default='')
    menu_remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="菜单备注",default='')
    parent_id: Mapped[str] = mapped_column(String(255),  nullable=True, comment="父级菜单id",default='')
    permission_id: Mapped[int] = mapped_column(nullable=True, comment="权限ID",default=0)
    sort_order: Mapped[int] = mapped_column(nullable=True, comment="排序 从校到大",default=0)

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)

    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
