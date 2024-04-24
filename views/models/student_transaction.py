from enum import Enum

from fastapi import Query
from pydantic import BaseModel, Field


class StudentTransactionStatus(str, Enum):
    """
    状态   待审批  已通过 已拒绝
    """
    # ALL = "All"

    NEEDAUDIT = "needaudit"

    PASS = "pass"
    REFUSE = "refuse"

    @classmethod
    def to_list(cls):
        return [cls.NEEDAUDIT, cls.PASS, cls.REFUSE]



class StudentEduInfo(BaseModel):
    student_id: int = Query(...,   description="学生id",min_length=1,max_length=20,examples=["1"],example="1"),
    province_id: str = Query(...,   description="省份",min_length=1,max_length=20,examples=["13000"],example="13000"),
    city_id: str = Query(...,   description="市",min_length=1,max_length=20,examples=["142323"]),
    area_id: str = Query(...,   description="区",min_length=1,max_length=20,examples=["1522000"]),
    district_id: str = Query(...,   description="区县",min_length=1,max_length=20,examples=["1622222"]),
    transfer_in_type: str = Query("",   description="转入类型",min_length=1,max_length=20,examples=["指定日期转入"]),
    natural_edu_no: str = Query("",   description="国家学籍号码",min_length=1,max_length=20,examples=["DF23321312"]),
    school_id: int  = Query(..., title="", description="学校ID",examples=["102"])
    school_name: str = Query(..., title="", description="学校名称",examples=["XXxiaoxue"])
    session: str = Query(..., title="", description="届别",examples=["2003"])
    attached_class: str = Query("", title="", description="附设班",examples=["3班"])
    grade_id: str = Query(..., title="", description="年级ID",examples=["102"])
    grade_name: str = Query(..., title="", description="年级",examples=["2年级"])
    class_id: str = Query(..., title="", description="班级id",examples=["125"])
    classes: str = Query(..., title="", description="班级",examples=["二2班"])
    major_id: str = Query(..., title="", description="专业",examples=["农业"])
    transferin_time:str= Query("", description="转入时间" ,min_length=1,max_length=20,examples=["2020-10-10"]),
    transferin_reason:str= Query("", description="转入原因" ,min_length=1,max_length=20,examples=["家庭搬迁..."]),
    status:str= Query('', description="" ,min_length=1,max_length=20,examples=["..."]),
    doc_upload: str = Field('',   description=" 附件",examples=[''])



class StudentTransaction(BaseModel):
    id:int= Query(None, title="", description="id", example='1'),
    in_school_id: int = Field(0, title="学校ID", description="学校ID",examples=['1'])
    grade_id: int = Field(0, title="年级ID", description="年级ID",examples=['1'])
    status: str = Field('', title="",description="状态",examples=[''])




class StudentTransactionFlow(BaseModel):
    """
    student_id: Mapped[int] = mapped_column(nullable=True , comment="学生ID",default=0)
    apply_id: Mapped[int] = mapped_column(nullable=True , comment="申请ID",default=0)

    stage: Mapped[str] = mapped_column(String(255),  nullable=True, comment="阶段",default='')
    description: Mapped[str] = mapped_column(String(255),  nullable=True, comment="流程描述",default='')
    remark: Mapped[str] = mapped_column(String(255),  nullable=True, comment="流程备注",default='')
    """
    id:int= Query(None, title="", description="id", example='1'),
    apply_id: int = Field(0, title="", description="转学申请ID",examples=['1'])
    status: str = Field('', title="",description="状态",examples=[''])
    stage: str = Field('', title="",description="阶段",examples=[''])

    description: str = Field('', title="",description="描述",examples=[''])
    remark: str = Field('', title="",description="备注",examples=[''])
    student_id: int = Field(0, title="", description="学生ID",examples=['1'])




