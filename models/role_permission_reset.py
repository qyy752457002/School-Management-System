from datetime import datetime

from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class RolePermissionReset(BaseDBModel):

    """
    角色权限
    """
    __tablename__ = 'lfun_role_permission_reset'
    __table_args__ = {'comment': '角色重构表权限表'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="班级ID",autoincrement=False)
    role_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="角色ID",default=0)
    menu_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="菜单ID",default=0)
    sort_order: Mapped[int] = mapped_column(nullable=True, comment="排序从小到大",default=0)
    remark: Mapped[str] = mapped_column(String(64),  nullable=True, comment="备注",default='')
    created_uid: Mapped[int] = mapped_column(  nullable=True , comment="创建人",default=0)
    updated_uid: Mapped[int] = mapped_column( nullable=True , comment="操作人",default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column( nullable=False  , comment="删除态",default=False)
