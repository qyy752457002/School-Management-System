from datetime import datetime
from enum import Enum
from typing import Iterable

from fastapi import Query
from pydantic import BaseModel, Field, model_validator

from models.student_transaction import AuditAction


class StudentTransactionType(str, Enum):
    """
    异动 类型  休学  转学  死亡  其他   用枚举 级联下拉
    """

    # ALL = "All"

    @classmethod
    def to_list(cls):
        return []


class StudentTransactionStatus(str, Enum):
    """
    状态   待审批  已通过 已拒绝
    """
    # ALL = "All"

    NEEDAUDIT = "needaudit"

    PASS = "pass"
    REFUSE = "refuse"
    CANCEL = "cancel"

    @classmethod
    def to_list(cls):
        return [cls.NEEDAUDIT, cls.PASS, cls.REFUSE, cls.CANCEL]


class StudentEduInfo(BaseModel):
    student_id: int | str | None = Query(..., description="学生id", title='学生id', min_length=1, max_length=20,
                                         examples=["1"], example="1"),
    province_id: str | None = Query('', description="省份", min_length=1, max_length=20, examples=["13000"],
                                    example="13000"),
    city_id: str | None = Query('', description="市", min_length=1, max_length=20, examples=["142323"]),
    area_id: str | None = Query('', description="区", min_length=1, max_length=20, examples=["1522000"]),
    district_id: str | None = Query('', description="区县", min_length=1, max_length=20, examples=["1622222"]),
    transfer_in_type: str | None = Query("", description="转入类型", min_length=1, max_length=20,
                                         examples=["指定日期转入"]),
    edu_number: str | None = Query("", description="国家学籍号码", min_length=1, max_length=20,
                                   examples=["DF23321312"]),
    school_id: int | str | None = Query(..., title="", description="学校ID", examples=["102"])
    school_name: str | None = Query('', title="", description="学校名称", examples=["XXxiaoxue"])
    session: str | None = Query('', title="", description="届别", examples=["2003"])
    attached_class: str | None = Query("", title="", description="附设班", examples=["3班"])
    grade_id: str | int | None = Query(..., title="", description="年级ID", examples=["102"])
    grade_name: str | None = Query('', title="", description="年级", examples=["2年级"])
    class_id: str | int | None = Query(..., title="", description="班级id", examples=["125"])
    classes: str | None = Query('', title="", description="班级", examples=["二2班"])
    major_id: str | int | None = Query(0, title="", description="专业", examples=["农业"])
    transfer_time: str | None = Query("", description="转学时间", min_length=1, max_length=20, examples=["2020-10-10"]),
    transfer_reason: str | None = Query("", description="转学原因", min_length=1, max_length=20,
                                        examples=["家庭搬迁..."]),
    status: str | None = Query('', description="", min_length=1, max_length=20, examples=["..."]),
    doc_upload: str | None = Field('', description=" 附件", examples=[''])
    doc_upload_url: str | None = Field('', title='附件url', description=" ", examples=[''])
    id: int | str | None = Query(0, description="id", examples=["1"], example="1"),
    relation_id: int | str | None = Query(0, description="关联id", examples=["1"], example="1"),
    remark: str | None = Query('', title="", description="", examples=["备注"])
    process_instance_id: int | None | str = Field(0, title="", description="", examples=['1'])
    created_at: datetime | None | str = Field(None, title="", description="", examples=['1'])
    updated_at: datetime | None | str = Field(None, title="", description="", examples=['1'])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'relation_id', 'process_instance_id',
                        'in_school_id', 'grade_id', 'transferin_audit_id']
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


class StudentEduInfoOut(BaseModel):
    student_id: int | str = Query(..., description="学生id", min_length=1, max_length=20, examples=["1"], example="1"),
    province_id: str | int = Query('', description="省份", min_length=1, max_length=20, examples=["13000"],
                                   example="13000"),
    city_id: str | int = Query('', description="市", min_length=1, max_length=20, examples=["142323"]),
    area_id: str | int = Query('', description="区", min_length=1, max_length=20, examples=["1522000"]),
    district_id: str | int = Query('', description="区县", min_length=1, max_length=20, examples=["1622222"]),
    transfer_in_type: str = Query("", description="转入类型", min_length=1, max_length=20, examples=["指定日期转入"]),
    country_no: str = Query("", description="国家学籍号码", min_length=1, max_length=20, examples=["DF23321312"]),
    school_id: int | str = Query(0, title="", description="学校ID", examples=["102"])
    school_name: str = Query(..., title="", description="学校名称", examples=["XXxiaoxue"])
    session: str = Query('', title="", description="届别", examples=["2003"])
    attached_class: str = Query("", title="", description="附设班", examples=["3班"])
    grade_id: str | int = Query('', title="", description="年级ID", examples=["102"])
    grade_name: str = Query(..., title="", description="年级", examples=["2年级"])
    class_id: str | int = Query('', title="", description="班级id", examples=["125"])
    classes: str = Query(..., title="", description="班级", examples=["二2班"])
    major_id: str | int = Query(0, title="", description="专业", examples=["农业"])
    transfer_time: str|None = Query("", description="转学时间", min_length=1, max_length=20, examples=["2020-10-10"]),
    transfer_reason: str = Query("", description="转学原因", min_length=1, max_length=20, examples=["家庭搬迁..."]),
    status: str = Query('', description="", min_length=1, max_length=20, examples=["..."]),
    doc_upload: str = Field('', description=" 附件", examples=[''])
    doc_upload_url: str | None = Field('', title='附件url', description=" ", examples=[''])

    id: int | str = Query(0, description="id", examples=["1"], example="1"),
    relation_id: int | str = Query(0, description="关联id", examples=["1"], example="1"),
    apply_user: str = Query('', title="", description="", examples=["申请人"])
    apply_time: str|None = Query('', title="", description="", examples=["申请时间"])
    student_gender: str | None = Query('', title="", description="", examples=[""])
    student_name: str | None = Query('', title="", description="", examples=[""])
    edu_number: str | None = Query("", description="国家学籍号码", min_length=1, max_length=30, examples=["DF23321312"])
    process_instance_id: int | str = Field(0, title="", description="", examples=['1'])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'relation_id', 'process_instance_id',
                        'in_school_id', 'grade_id', 'transferin_audit_id']
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


class StudentTransaction(BaseModel):
    id: int | str = Query(None, title="", description="id", example='1'),
    in_school_id: int | str = Field(0, title="学校ID", description="学校ID", examples=['1'])
    grade_id: int | str = Field(0, title="年级ID", description="年级ID", examples=['1'])
    process_instance_id: int | str = Field(0, title="", description="", examples=['1'])
    status: str = Field('', title="", description="状态", examples=[''])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'relation_id', 'process_instance_id',
                        'in_school_id', 'grade_id', 'transferin_audit_id']
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


class StudentTransactionFlow(BaseModel):
    """
    student_id: Mapped[int] = mapped_column(nullable=True , comment="学生ID",default=0)
    apply_id: Mapped[int] = mapped_column(nullable=True , comment="申请ID",default=0)

    stage: Mapped[str] = mapped_column(String(255),  nullable=True, comment="阶段",default='')
    description: Mapped[str] = mapped_column(String(255),  nullable=True, comment="流程描述",default='')
    remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="流程备注",default='')
    """
    id: int | str = Query(None, title="", description="id", example='1'),
    apply_id: int | str = Field(0, title="", description="转学申请ID", examples=['1'])
    status: str = Field('', title="", description="状态", examples=[''])
    stage: str = Field('', title="", description="阶段", examples=[''])

    description: str = Field('', title="", description="描述", examples=[''])
    remark: str = Field('', title="", description="备注", examples=[''])
    student_id: int | str = Field(0, title="", description="学生ID", examples=['1'])

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'relation_id', 'process_instance_id',
                        'in_school_id', 'grade_id', 'transferin_audit_id']
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


class StudentTransactionAudit(BaseModel):
    transferin_audit_id: int | str = Query(0, description="转入申请id", example='2')
    process_instance_id: int | str = Query(0, description="流程实例ID", example='2')
    transferin_audit_action: AuditAction = Query(..., description="审批的操作",
                                                 example='pass')
    remark: str = Query("", description="审批的备注", min_length=0, max_length=200,
                        example='同意 无误')

    @model_validator(mode="before")
    @classmethod
    def check_id_before(self, data: dict):
        _change_list = ["id", 'student_id', 'school_id', 'class_id', 'session_id', 'relation_id', 'process_instance_id',
                        'in_school_id', 'grade_id', 'transferin_audit_id']
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


class StudentTransactionPageSearch(BaseModel):
    audit_status: StudentTransactionStatus = Query("", title="", description="状态", examples=['needaudit'])
    student_name: str = Query("", title="", description="学生姓名", min_length=1, max_length=20),

    school_id: int = Query(0, title="", description="学校ID", )
    school_name: str  = Query('', title="", description="学校", )
    student_gender: str = Query("", title="", description=" 学生性别", min_length=1, max_length=20)

    applicant_name: str = Query("",alias='apply_user', title="", description="申请人", min_length=1, max_length=20, )
    edu_number: str = Query("",alias='edu_no', title="  ", description=" 学籍号码", min_length=1, max_length=20)
