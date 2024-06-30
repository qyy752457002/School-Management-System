from datetime import datetime
from enum import Enum

from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel


class TransactionDirection(str, Enum):
    """
    转学方向
    """
    OUT = "out"
    IN = "in"

    @classmethod
    def to_list(cls):
        return [cls.OUT, cls.IN]


class AuditAction(str, Enum):
    """
    审核操作
    """
    NEEDAUDIT = "needaudit"

    PASS = "pass"
    REFUSE = "refuse"
    CANCEL = "canel"

    @classmethod
    def to_list(cls):
        return [cls.NEEDAUDIT,cls.PASS, cls.REFUSE, cls.CANCEL]

class AuditFlowStatus(str, Enum):
    """
    流程 的状态定义
    """
    FLOWBEGIN = "flow_begin"
    APPLY_SUBMIT = "apply_submit"
    PASS = "pass"
    REFUSE = "refuse"
    RECEIVECOMPLETED = "refuse"
    FLOWEND = "flow_begin"

    @classmethod
    def to_list(cls):
        return [cls.FLOWBEGIN,cls.APPLY_SUBMIT, cls.PASS, cls.REFUSE, cls.RECEIVECOMPLETED, cls.FLOWEND]


class StudentTransaction(BaseDBModel):
    """
    转学休学入学毕业申请表
    grade_name: str = Query(..., title="", description="年级",examples=["2年级"])
 classes: str = Query(..., title="", description="班级",examples=["二2班"])
transfer_time:str= Query("", description="转入/出时间" ,min_length=1,max_length=20,examples=["2020-10-10"]),
transfer_reason:str= Query("", description="转学原因" ,min_length=1,max_length=20,examples=["家庭搬迁..."]),
doc_upload: str = Field('',   description=" 附件",examples=[''])
    """
    __tablename__ = 'lfun_student_transaction'
    __table_args__ = {'comment': '转学休学入学毕业申请表'}

    id: Mapped[int] = mapped_column(primary_key=True, comment="班级ID", autoincrement=True)
    school_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="学校名称", default='')
    grade_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="年级", default='')
    classes: Mapped[str] = mapped_column(String(255), nullable=True, comment="班级", default='')
    transfer_time: Mapped[str] = mapped_column(String(255), nullable=True, comment="转入/出时间", default='')
    transfer_reason: Mapped[str] = mapped_column(String(255), nullable=True, comment="转学原因", default='')
    doc_upload: Mapped[str] = mapped_column(String(255), nullable=True, comment="附件", default='')
    process_instance_id: Mapped[int] = mapped_column(  nullable=True, comment="流程ID", default=0)

    student_id: Mapped[int] = mapped_column(nullable=True, comment="学生ID", default=0)
    student_no: Mapped[str] = mapped_column(String(255), nullable=True, comment="学号", default='')
    student_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="学生姓名", default='')

    current_org: Mapped[str] = mapped_column(String(255), nullable=True, comment="当前机构", default='')
    apply_user: Mapped[str] = mapped_column(String(255), nullable=True, comment="申请人", default='')
    apply_time: Mapped[str] = mapped_column(String(255), nullable=True, comment="申请时间", default='')
    school_id: Mapped[int] = mapped_column(nullable=True, comment="学校ID", default=0)
    relation_id: Mapped[int] = mapped_column(nullable=True, comment="关联学校ID", default=0)


    transaction_type: Mapped[str] = mapped_column(String(30), nullable=True, comment="异动类型", default='')
    transaction_type_lv2: Mapped[str] = mapped_column(String(30), nullable=True, comment="异动类型2级", default='')

    country_no: Mapped[str] = mapped_column(String(255), nullable=True, comment="国家学籍号码", default='')
    # out_date: Mapped[str] = mapped_column(String(255), nullable=True, comment="转出日期", default='')
    reason: Mapped[str] = mapped_column(String(255), nullable=True, comment="转学原因", default='')

    province_id: Mapped[str] = mapped_column(String(30), nullable=True, comment="省份", default='')
    city_id: Mapped[str] = mapped_column(String(30), nullable=True, comment="市", default='')
    district_id: Mapped[str] = mapped_column(String(30), nullable=True, comment="区县", default='')
    area_id: Mapped[str] = mapped_column(String(30), nullable=True, comment="区", default='')
    direction: Mapped[str] = mapped_column(String(30), nullable=True, comment="出入方向", default='')
    transfer_in_type: Mapped[str] = mapped_column(String(30), nullable=True, comment="转入类型", default='')
    session: Mapped[str] = mapped_column(String(30), nullable=True, comment="届别", default='')
    attached_class: Mapped[str] = mapped_column(String(30), nullable=True, comment="附设班", default='')
    grade_id: Mapped[str] = mapped_column(String(30), nullable=True, comment="年级ID", default='')

    class_id: Mapped[str] = mapped_column(String(30), nullable=True, comment="班级id", default='')


    major_id: Mapped[str] = mapped_column(String(30), nullable=True, comment="专业id", default='')
    major_name: Mapped[str] = mapped_column(String(30), nullable=True, comment="专业", default='')
    remark: Mapped[str] = mapped_column(String(255), nullable=True, comment="备注", default='')
    status: Mapped[str] = mapped_column(String(64), nullable=True, comment="状态", default='')

    is_valid: Mapped[bool] = mapped_column(nullable=False, comment="是否有效", default=True)

    created_uid: Mapped[int] = mapped_column(nullable=True, comment="创建人", default=0)
    updated_uid: Mapped[int] = mapped_column(nullable=True, comment="操作人", default=0)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = mapped_column(DateTime, onupdate=datetime.now, default=datetime.now, nullable=False,
                               comment="更新时间")
    is_deleted: Mapped[bool] = mapped_column(nullable=False, comment="删除态", default=False)
