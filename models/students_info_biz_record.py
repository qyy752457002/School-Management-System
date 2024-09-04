from sqlalchemy import String, Date, BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date


class StudentInfoBizRecord(BaseDBModel):
    """
    学生信息业务记录表 含 (升级 留级 届别等等 )

    """
    __tablename__ = 'lfun_students_info_biz_record'
    __table_args__ = {'comment': '学生信息业务记录表'}

    id: Mapped[int] = mapped_column(BigInteger,primary_key=True, comment="主键",   autoincrement=False)
    student_base_id: Mapped[int] = mapped_column(BigInteger, nullable=True, comment="",default=0, autoincrement=False)

    student_id: Mapped[int] = mapped_column(BigInteger,nullable=False, comment="学生ID",default=0, autoincrement=False)

    name_pinyin: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="姓名拼音")

    session: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="届别")
    session_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="届别id", default=0)
    edu_number: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学籍号")
    student_number: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学号")
    graduation_type: Mapped[str] = mapped_column(String(10), nullable=True, default='', comment="毕业类型")
    graduation_remarks: Mapped[str] = mapped_column(String(255), nullable=True, default='', comment="毕业备注")
    credential_notes: Mapped[str] = mapped_column(String(255), nullable=True, default='', comment="制证备注")
    graduation_photo: Mapped[str] = mapped_column(String(255), nullable=True, default='', comment="毕业照")

    grade: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="年级")
    classroom: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="班级")
    class_number: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="班号")
    class_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="班级id", default=0)
    grade_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="年级id", default=0)

    school_id: Mapped[int] = mapped_column(BigInteger,nullable=True, comment="学校id", default=0)
    # 户口所在地(residence_district) 户籍地址修改为户口所在地（详细）(residence_address)
    school: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="学校")
    registration_date: Mapped[date] = mapped_column(Date, nullable=True, default=date(1970, 1, 1), comment="登记日期")

    birth_place: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="出生地")
    residence_district: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="户口所在地new")

    enrollment_date: Mapped[date] = mapped_column(Date, default=date(1970, 1, 1), nullable=True, comment="入学日期")
    # 入学年月(admission_date)健康状况(health_status)
    admission_date: Mapped[date] = mapped_column(Date, default=date(1970, 1, 1), nullable=True, comment="入学年月new")
    contact_number: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="联系电话")
    health_condition: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="健康状况")
    health_status: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="枚举health_status")
    political_status: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="政治面貌")
    ethnicity: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="民族")

    communication_district: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="通信地址行政区")
    postal_code: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="邮政编码")
    communication_address: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="通信地址")
    photo_upload_time: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="照片上传时间")
    identity_card_validity_period: Mapped[str] = mapped_column(String(64), default='', nullable=True,
                                                               comment="身份证件有效期")
    specialty: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="特长")
    permanent_address: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="常住地址")
    remark: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="备注", )
    county: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment="区县")
    emporary_borrowing_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="临时借读状态",default="Y")
    identity: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份",default='')
    identity_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份类型",default='')
    nationality: Mapped[str] = mapped_column(String(64), nullable=True, comment="国籍/地区",default='')
    enrollment_method: Mapped[str] = mapped_column(String(64), nullable=True, comment="就读方式枚举enrollment_method",default='')

    flow_out_time: Mapped[str] = mapped_column(String(64), default='', nullable=True, comment="流出时间")
    flow_out_reason: Mapped[str] = mapped_column(String(64), nullable=True, comment="流出原因")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
