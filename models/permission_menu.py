from datetime import datetime

from sqlalchemy import String, DateTime
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

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    menu_name: Mapped[str] = mapped_column(String(255),  nullable=True, comment="菜单名称",default='')
    menu_path: Mapped[str] = mapped_column(String(255),  nullable=True, comment="菜单路径",default='')
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


    @staticmethod
    def seed():
        return [

            PermissionMenu(id=1, menu_name="园所信息管理（规划）", menu_path="/planning", menu_icon="", menu_type="menu", menu_code="planning", menu_status="", menu_remark="", parent_id="0", permission_id=1, sort_order=0,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False  ),
            PermissionMenu(id=2, menu_name="园所信息管理（学校）", menu_path="/school", menu_icon="", menu_type="menu", menu_code="school", menu_status="", menu_remark="", parent_id="0", permission_id=1, sort_order=0,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False  ),
            PermissionMenu(id=3, menu_name="园所配置管理", menu_path="", menu_icon="", menu_type="root", menu_code="config", menu_status="", menu_remark="", parent_id="0", permission_id=1, sort_order=0,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False  ),

            PermissionMenu(id=4, menu_name="年级管理", menu_path="/grade", menu_icon="", menu_type="menu", menu_code="grade", menu_status="", menu_remark="", parent_id="3", permission_id=1, sort_order=0,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False  ),

            PermissionMenu(id=5, menu_name="班级管理", menu_path="/class", menu_icon="", menu_type="menu", menu_code="class", menu_status="", menu_remark="", parent_id="3", permission_id=1, sort_order=0,created_uid=0,updated_uid=0,created_at=datetime.now(),updated_at=datetime.now(),is_deleted=False  ),

        ]



