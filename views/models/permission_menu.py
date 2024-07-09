from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field, model_validator


class PermissionMenu(BaseModel):
    """
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
    """

    created_at: datetime = Field('',  description="简介",examples=['2020-01-01'])
    id:int|str= Query(0, title="", description="id", example='1')
    power_name: str = Query('', title="", description="菜单名称", example='1')
    power_url: str = Query('', title="", description="菜单路径", example='1')
    # menu_icon: str = Query(None, title="", description="菜单图标", example='1')
    power_type: str = Query('', title="", description="菜单类型", example='1')
    power_code: str = Query('', title="", description="菜单简码", example='1')
    # menu_status: str = Query(None, title="", description="菜单状态", example='1')
    # menu_remark: str = Query(None, title="", description="菜单备注", example='1')
    parent_id: str = Query('', title="", description="父级菜单id", example='1')
    permission_id: int|str = Query(0, title="", description="权限ID", example='1')
    sort_order: int = Query(0, title="", description="排序 从校到大", example='1')
    children: list = Query([], title="", description="", example= [])
    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list= ["id",'permission_id']
        for _change in _change_list:
            if _change not in data:
                continue
            if isinstance(data[_change], str):
                data[_change] = int(data[_change])
            elif isinstance(data[_change], int):
                pass
            else:
                pass
        return data



