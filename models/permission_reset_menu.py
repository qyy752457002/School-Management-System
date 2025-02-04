from datetime import datetime

from mini_framework.databases.entities import BaseDBModel
from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import mapped_column, Mapped


class PermissionResetMenu(BaseDBModel):
    """
    菜单权限表
    权限id
    父级菜单id

    """
    __tablename__ = 'lfun_permission_reset_menu'
    __table_args__ = {'comment': '菜单重构权限表'}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="班级ID", autoincrement=False)
    app_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="系统名称", default='')
    menu_name: Mapped[str] = mapped_column(String(64), nullable=True, comment="菜单名称", default='')
    menu_path: Mapped[str] = mapped_column(String(64), nullable=True, comment="菜单路径", default='')
    resource_code: Mapped[str] = mapped_column(String(128), nullable=True, comment="资源编码-用于资源和菜单的绑定",
                                               default='')
    action: Mapped[str] = mapped_column(String(600), nullable=True, comment="允许的资源动作", default='')
    menu_icon: Mapped[str] = mapped_column(String(255), nullable=True, comment="菜单图标", default='')
    menu_type: Mapped[str] = mapped_column(String(255), nullable=True, comment="菜单类型", default='')
    menu_code: Mapped[str] = mapped_column(String(255), nullable=True, comment="菜单简码", default='')
    menu_status: Mapped[str] = mapped_column(String(255), nullable=True, comment="菜单状态", default='')
    menu_remark: Mapped[str] = mapped_column(String(255), nullable=True, comment="菜单备注", default='')
    parent_id: Mapped[str] = mapped_column(String(255), nullable=True, comment="父级菜单id", default='')
    permission_id: Mapped[int] = mapped_column(nullable=True, comment="权限ID", default=0)
    sort_order: Mapped[int] = mapped_column(nullable=True, comment="排序 从校到大", default=0)
    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=True, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=True, comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)

    @staticmethod
    def seed():
        return [
            PermissionResetMenu(id=1, app_name="幼儿园园所信息管理系统（xxx）", menu_name="园所信息管理（规划口径）",
                                menu_path="/planning", resource_code="", action="", menu_icon="", menu_type="menu",
                                menu_code="planning", menu_status="None", menu_remark="", parent_id="0",
                                permission_id=0,
                                sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=2, app_name="幼儿园园所信息管理系统（xxx）", menu_name="园所信息管理",
                                menu_path="/school",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="school",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=3, app_name="幼儿园园所信息管理系统（xxx）", menu_name="园所配置管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="config",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=4, app_name="幼儿园园所信息管理系统（xxx）", menu_name="班级类型管理",
                                menu_path="/grade",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="grade",
                                menu_status="None", menu_remark="", parent_id="3", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=5, app_name="幼儿园园所信息管理系统（xxx）", menu_name="班级管理", menu_path="/class",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="class",
                                menu_status="None", menu_remark="", parent_id="3", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=6, app_name="幼儿园园所信息管理系统（xxx）", menu_name="组织架构管理",
                                menu_path="/org",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="org",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=7, app_name="幼儿园园所信息管理系统（xxx）", menu_name="资产管理",
                                menu_path="/asset-manage", resource_code="", action="", menu_icon="", menu_type="menu",
                                menu_code="asset-manage", menu_status="None", menu_remark="", parent_id="0",
                                permission_id=0,
                                sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=8, app_name="幼儿园园所信息管理系统（xxx）", menu_name="校舍管理",
                                menu_path="/school-house", resource_code="", action="", menu_icon="", menu_type="menu",
                                menu_code="school-house", menu_status="None", menu_remark="", parent_id="0",
                                permission_id=0,
                                sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=9, app_name="中小学学校信息管理系统", menu_name="学校信息管理（规划口径）",
                                menu_path="/planning", resource_code="", action="", menu_icon="", menu_type="menu",
                                menu_code="planning", menu_status="None", menu_remark="", parent_id="0",
                                permission_id=0,
                                sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=10, app_name="中小学学校信息管理系统", menu_name="学校信息管理", menu_path="/school",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="school",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=11, app_name="中小学学校信息管理系统", menu_name="学校配置管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="config",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=12, app_name="中小学学校信息管理系统", menu_name="年级管理", menu_path="/grade",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="grade",
                                menu_status="None", menu_remark="", parent_id="11", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=13, app_name="中小学学校信息管理系统", menu_name="班级管理", menu_path="/class",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="class",
                                menu_status="None", menu_remark="", parent_id="11", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=14, app_name="中小学学校信息管理系统", menu_name="学科管理", menu_path="/course",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="course",
                                menu_status="None", menu_remark="", parent_id="11", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=15, app_name="中小学学校信息管理系统", menu_name="课程管理", menu_path="/subject",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="subject",
                                menu_status="None", menu_remark="", parent_id="11", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=16, app_name="中小学学校信息管理系统", menu_name="组织架构管理", menu_path="/org",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="org",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=17, app_name="中小学学校信息管理系统", menu_name="资产管理",
                                menu_path="/asset-manage",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="asset-manage",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=18, app_name="中小学学校信息管理系统", menu_name="校舍管理",
                                menu_path="/school-house",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="school-house",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=19, app_name="中等职业学校信息管理系统", menu_name="学校信息管理（规划口径）",
                                menu_path="/planning", resource_code="", action="", menu_icon="", menu_type="menu",
                                menu_code="planning", menu_status="None", menu_remark="", parent_id="0",
                                permission_id=0,
                                sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=20, app_name="中等职业学校信息管理系统", menu_name="学校信息管理",
                                menu_path="/school",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="school",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=21, app_name="中等职业学校信息管理系统", menu_name="职高配置管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="config",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=22, app_name="中等职业学校信息管理系统", menu_name="专业管理", menu_path="/major",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="major",
                                menu_status="None", menu_remark="", parent_id="21", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=23, app_name="中等职业学校信息管理系统", menu_name="年级管理", menu_path="/grade",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="grade",
                                menu_status="None", menu_remark="", parent_id="21", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=24, app_name="中等职业学校信息管理系统", menu_name="班级管理", menu_path="/class",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="class",
                                menu_status="None", menu_remark="", parent_id="21", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=25, app_name="中等职业学校信息管理系统", menu_name="课程管理", menu_path="/subject",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="subject",
                                menu_status="None", menu_remark="", parent_id="21", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=26, app_name="中等职业学校信息管理系统", menu_name="组织架构管理", menu_path="/org",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="org",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=27, app_name="中等职业学校信息管理系统", menu_name="资产管理",
                                menu_path="/asset-manage",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="asset-manage",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=28, app_name="中等职业学校信息管理系统", menu_name="校舍管理",
                                menu_path="/school-house",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="school-house",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=29, app_name="教职工信息管理系统", menu_name="新教职工信息管理",
                                menu_path="/onboarding",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="onboarding",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=30, app_name="教职工信息管理系统", menu_name="在职教职工信息管理",
                                menu_path="/employed",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="employed",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=31, app_name="教职工信息管理系统", menu_name="教职工变动管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="alteration",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=32, app_name="教职工信息管理系统", menu_name="借动管理",
                                menu_path="/alteration/borrowing", resource_code="", action="", menu_icon="",
                                menu_type="menu", menu_code="alterationborrowing", menu_status="None", menu_remark="",
                                parent_id="31", permission_id=0, sort_order=0, created_uid=0, updated_uid=0,
                                created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=33, app_name="教职工信息管理系统", menu_name="调动管理",
                                menu_path="/alteration/transfer",
                                resource_code="", action="", menu_icon="", menu_type="menu",
                                menu_code="alterationtransfer",
                                menu_status="None", menu_remark="", parent_id="31", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=34, app_name="教职工信息管理系统", menu_name="其他变动管理",
                                menu_path="/alteration/other", resource_code="", action="", menu_icon="",
                                menu_type="menu",
                                menu_code="alterationother", menu_status="None", menu_remark="", parent_id="31",
                                permission_id=0, sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=35, app_name="教职工信息管理系统", menu_name="非在职教职工管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="nonemployed",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=36, app_name="教职工信息管理系统", menu_name="离退休教职工管理",
                                menu_path="/nonemployed/retire", resource_code="", action="", menu_icon="",
                                menu_type="menu",
                                menu_code="nonemployedretire", menu_status="None", menu_remark="", parent_id="35",
                                permission_id=0, sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=37, app_name="教职工信息管理系统", menu_name="非离退休教职工管理",
                                menu_path="/nonemployed/noretire", resource_code="", action="", menu_icon="",
                                menu_type="menu", menu_code="nonemployednoretire", menu_status="None", menu_remark="",
                                parent_id="35", permission_id=0, sort_order=0, created_uid=0, updated_uid=0,
                                created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=38, app_name="教职工信息管理系统", menu_name="系统管理", menu_path="",
                                resource_code="",
                                action="", menu_icon="", menu_type="root", menu_code="trchsys", menu_status="None",
                                menu_remark="", parent_id="0", permission_id=0, sort_order=0, created_uid=0,
                                updated_uid=0,
                                created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=39, app_name="教职工信息管理系统", menu_name="信息配置", menu_path="/trchsys/info",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="trchsysinfo",
                                menu_status="None", menu_remark="", parent_id="38", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=40, app_name="中小学学生信息管理系统", menu_name="在读学生管理",
                                menu_path="/nowstudent",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="/nowstudent",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=41, app_name="中小学学生信息管理系统", menu_name="学生变动管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="instudent",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=42, app_name="中小学学生信息管理系统", menu_name="转学学生管理",
                                menu_path="/instudent",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="instudent",
                                menu_status="None", menu_remark="", parent_id="41", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=43, app_name="中小学学生信息管理系统", menu_name="异动管理",
                                menu_path="/instudent/innerTransfer", resource_code="", action="", menu_icon="",
                                menu_type="menu", menu_code="instudent_innerTransfer", menu_status="None",
                                menu_remark="",
                                parent_id="41", permission_id=0, sort_order=0, created_uid=0, updated_uid=0,
                                created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=44, app_name="中小学学生信息管理系统", menu_name="非在读学生管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="notinstudent",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=45, app_name="中小学学生信息管理系统", menu_name="毕业学生管理",
                                menu_path="/notinstudent/graduate", resource_code="", action="", menu_icon="",
                                menu_type="menu", menu_code="notinstudent_graduate", menu_status="None", menu_remark="",
                                parent_id="44", permission_id=0, sort_order=0, created_uid=0, updated_uid=0,
                                created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=46, app_name="中小学学生信息管理系统", menu_name="其他非在读管理",
                                menu_path="/notinstudent/other", resource_code="", action="", menu_icon="",
                                menu_type="menu",
                                menu_code="notinstudent_other", menu_status="None", menu_remark="", parent_id="44",
                                permission_id=0, sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=47, app_name="中小学学生信息管理系统", menu_name="审核管理", menu_path="/stuaudit",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="stuaudit",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=48, app_name="中小学学生信息管理系统", menu_name="毕业证管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="diploma",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=49, app_name="中小学学生信息管理系统", menu_name="制证批次",
                                menu_path="/diploma/batch",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="diploma_batch",
                                menu_status="None", menu_remark="", parent_id="48", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=50, app_name="中小学学生信息管理系统", menu_name="制证模板",
                                menu_path="/diploma/template", resource_code="", action="", menu_icon="",
                                menu_type="menu",
                                menu_code="diploma_template", menu_status="None", menu_remark="", parent_id="48",
                                permission_id=0, sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=51, app_name="中小学学生信息管理系统", menu_name="毕业证书",
                                menu_path="/diploma/certificate", resource_code="", action="", menu_icon="",
                                menu_type="menu", menu_code="diploma_certificate", menu_status="None", menu_remark="",
                                parent_id="48", permission_id=0, sort_order=0, created_uid=0, updated_uid=0,
                                created_at=datetime.now(), updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=52, app_name="中小学学生信息管理系统", menu_name="制证公司",
                                menu_path="/diploma/company",
                                resource_code="", action="", menu_icon="", menu_type="menu",
                                menu_code="diploma_company",
                                menu_status="None", menu_remark="", parent_id="48", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=53, app_name="中小学学生信息管理系统", menu_name="系统管理", menu_path="",
                                resource_code="", action="", menu_icon="", menu_type="root", menu_code="trchsys",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=54, app_name="中小学学生信息管理系统", menu_name="信息配置",
                                menu_path="/trchsys/info",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="trchsys_info",
                                menu_status="None", menu_remark="", parent_id="53", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=55, app_name="事业单位信息管理系统", menu_name="单位信息管理",
                                menu_path="/institution/sy", resource_code="", action="", menu_icon="",
                                menu_type="menu",
                                menu_code="institution-sy", menu_status="None", menu_remark="", parent_id="0",
                                permission_id=0, sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=56, app_name="事业单位信息管理系统", menu_name="组织架构管理", menu_path="/org",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="org",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),
            PermissionResetMenu(id=57, app_name="行政单位信息管理系统", menu_name="单位信息管理",
                                menu_path="/institution/sy", resource_code="", action="", menu_icon="",
                                menu_type="menu",
                                menu_code="institution-sy", menu_status="None", menu_remark="", parent_id="0",
                                permission_id=0, sort_order=0, created_uid=0, updated_uid=0, created_at=datetime.now(),
                                updated_at=datetime.now(), is_deleted=False),
            PermissionResetMenu(id=58, app_name="行政单位信息管理系统", menu_name="组织架构管理", menu_path="/org",
                                resource_code="", action="", menu_icon="", menu_type="menu", menu_code="org",
                                menu_status="None", menu_remark="", parent_id="0", permission_id=0, sort_order=0,
                                created_uid=0, updated_uid=0, created_at=datetime.now(), updated_at=datetime.now(),
                                is_deleted=False),

        ]
