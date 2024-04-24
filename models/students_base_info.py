from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped

from mini_framework.databases.entities import BaseDBModel

from datetime import date


class StudentBaseInfo(BaseDBModel):
    """
    学生id：student_id
    姓名拼音：name_pinyin
    届别：session
    年级：grade
    班级：classroom
    班号：class_number
    学校：school
    登记日期：registration_date
    户籍地址：residence_address
    户口所在行政区：residence_district
    出生地行政区：birthplace_district
    籍贯行政区：native_place_district
    宗教信仰：religious_belief
    户口性质：residence_nature
    入学日期：enrollment_date
    联系电话：contact_number
    健康状况：health_condition
    政治面貌：political_status
    民族：ethnicity
    血型：blood_type
    家庭电话：home_phone_number
    电子信箱/其他联系方式：email_or_other_contact
    是否随迁子女：migrant_children
    是否残疾人：disabled_person
    是否独生子女：only_child
    是否留守儿童：left_behind_children
    是否流动人口：floating_population
    是否港澳台侨胞：overseas_chinese
    户口所在地（详细）：residence_address_detail
    通信地址行政区：communication_district
    邮政编码：postal_code
    通信地址：communication_address
    照片上传时间：photo_upload_time
    身份证件有效期：identity_card_validity_period
    特长：specialty
    常住地址：permanent_address
    备注：remark
    临时借读状态：temporary_borrowing_status
    流出时间：flow_out_time
    流出原因：flow_out_reason
    """
    __tablename__ = 'lfun_students_base_info'
    __table_args__ = {'comment': '学生表基本信息模型'}

    student_base_id: Mapped[int] = mapped_column(primary_key=True, comment="主键", autoincrement=True)  # 与学生表关联，关系为一对一，主键
    student_id: Mapped[int] = mapped_column(nullable=False,comment="学生ID", autoincrement=True)  # 与学生表关联，关系为一对一，主键
    name_pinyin: Mapped[str] = mapped_column(String(64), nullable=True, comment="姓名拼音")
    session: Mapped[str] = mapped_column(String(64), nullable=True, comment="届别")
    grade: Mapped[str] = mapped_column(String(64), nullable=True, comment="年级")
    classroom: Mapped[str] = mapped_column(String(64), nullable=True, comment="班级")
    class_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="班号")
    school: Mapped[str] = mapped_column(String(64), nullable=True, comment="学校")
    registration_date: Mapped[date] = mapped_column(Date, default=None, nullable=True, comment="登记日期")
    residence_address: Mapped[str] = mapped_column(String(64), nullable=False, comment="户籍地址")
    residence_district: Mapped[str] = mapped_column(String(64), nullable=False, comment="户口所在行政区")
    birthplace_district: Mapped[str] = mapped_column(String(64), nullable=False, comment="出生地")
    native_place_district: Mapped[str] = mapped_column(String(64), nullable=False, comment="籍贯")
    religious_belief: Mapped[str] = mapped_column(String(64), nullable=True, comment="宗教信仰")
    residence_nature: Mapped[str] = mapped_column(String(64), nullable=False, comment="户口性质")
    enrollment_date: Mapped[date] = mapped_column(Date, default=None, nullable=True, comment="入学日期")
    contact_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="联系电话")
    health_condition: Mapped[str] = mapped_column(String(64), nullable=False, comment="健康状况")
    political_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="政治面貌")
    ethnicity: Mapped[str] = mapped_column(String(64), nullable=True, comment="民族")
    blood_type: Mapped[str] = mapped_column(String(64), nullable=True, comment="血型")
    home_phone_number: Mapped[str] = mapped_column(String(64), nullable=True, comment="家庭电话")
    email_or_other_contact: Mapped[str] = mapped_column(String(64), nullable=True, comment="电子信箱/其他联系方式")
    migrant_children: Mapped[str] = mapped_column(String(64), nullable=True, comment="是否随迁子女")
    disabled_person: Mapped[str] = mapped_column(String(64), nullable=True, comment="是否残疾人")
    only_child: Mapped[str] = mapped_column(String(64), nullable=True, comment="是否独生子女")
    left_behind_children: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否留守儿童")
    floating_population: Mapped[str] = mapped_column(String(64), nullable=False, comment="是否流动人口")
    overseas_chinese: Mapped[str] = mapped_column(String(64), nullable=True, comment="是否港澳台侨胞")
    residence_address_detail: Mapped[str] = mapped_column(String(64), nullable=True, comment="户口所在地（详细）")
    communication_district: Mapped[str] = mapped_column(String(64), nullable=True, comment="通信地址行政区")
    postal_code: Mapped[str] = mapped_column(String(64), nullable=True, comment="邮政编码")
    communication_address: Mapped[str] = mapped_column(String(64), nullable=True, comment="通信地址")
    photo_upload_time: Mapped[str] = mapped_column(String(64), nullable=True, comment="照片上传时间")
    identity_card_validity_period: Mapped[str] = mapped_column(String(64), nullable=True, comment="身份证件有效期")
    specialty: Mapped[str] = mapped_column(String(64), nullable=True, comment="特长")
    permanent_address: Mapped[str] = mapped_column(String(64), nullable=True, comment="常住地址")
    remark: Mapped[str] = mapped_column(String(64), nullable=True, comment="备注", )
    emporary_borrowing_status: Mapped[str] = mapped_column(String(64), nullable=True, comment="临时借读状态",
                                                           default="否")
    flow_out_time: Mapped[str] = mapped_column(String(64), default='', nullable=True, comment="流出时间")
    flow_out_reason: Mapped[str] = mapped_column(String(64), nullable=True, comment="流出原因")
    is_deleted: Mapped[bool] = mapped_column(default=False, comment="是否删除")
