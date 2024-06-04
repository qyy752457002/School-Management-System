from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class RolePermission(BaseDBModel):

    """
    角色权限
    """
    __tablename__ = 'lfun_role_permission'
    __table_args__ = {'comment': '角色权限表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID",autoincrement=True)
    role_id: Mapped[int] = mapped_column(nullable=True, comment="角色ID",default=0)
    menu_id: Mapped[int] = mapped_column(nullable=True, comment="菜单ID",default=0)
    sort_order: Mapped[int] = mapped_column(nullable=True, comment="排序从小到大",default=0)
    remark: Mapped[str] = mapped_column(String(64),  nullable=True, comment="备注",default='')

    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)

    @staticmethod
    def seed():
        return [
            RolePermission(id=1, role_id=1, menu_id=1, sort_order=1, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            RolePermission(id=2,role_id=1, menu_id=2, sort_order=1, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            RolePermission(id=3,role_id=1, menu_id=3, sort_order=1, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            RolePermission(id=4,role_id=1, menu_id=4, sort_order=1, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            RolePermission(id=5,role_id=1, menu_id=5, sort_order=1, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            RolePermission(id=6,role_id=1, menu_id=6, sort_order=1, created_uid=1, updated_uid=1, created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
        ]


